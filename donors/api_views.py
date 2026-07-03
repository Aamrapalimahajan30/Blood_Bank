from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from donors.documents import (
    DonorDocument, CampDocument, BloodRequestDocument,
    get_donors_by_group_and_location, camp_donor_count_report,
)
from donors.serializers import DonorSerializer, CampSerializer, BloodRequestSerializer
from donors.core import BloodRequest, MatchEngine
from donors.notifications import notify_matched_donors
from donors.exceptions import NoMatchingDonorError, BloodBankError


def _doc_to_dict(doc, extra=None):
    d = {
        'id': str(doc.id),
        **{f: getattr(doc, f) for f in doc._fields if f != 'id'}
    }
    if extra:
        d.update(extra)
    return d


class DonorListAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        blood_group = request.query_params.get('blood_group')
        location = request.query_params.get('location')

        qs = DonorDocument.objects
        if blood_group:
            qs = qs.filter(blood_group=blood_group.upper())
        if location:
            qs = qs.filter(location__iexact=location)

        data = [_doc_to_dict(d) for d in qs]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DonorSerializer(data=request.data)
        if serializer.is_valid():
            donor = DonorDocument(**serializer.validated_data).save()
            return Response(_doc_to_dict(donor), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CampListAPI(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request):
        camps = CampDocument.objects.order_by('camp_date')
        data = [_doc_to_dict(c, extra={'donor_count': len(c.registered_donors)}) for c in camps]
        return Response(data)

    def post(self, request):
        serializer = CampSerializer(data=request.data)
        if serializer.is_valid():
            payload = {k: v for k, v in serializer.validated_data.items() if k != 'donor_count'}
            camp = CampDocument(**payload).save()
            return Response(_doc_to_dict(camp), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BloodRequestListAPI(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request):
        reqs = BloodRequestDocument.objects.order_by('-created_at')
        data = [_doc_to_dict(r) for r in reqs]
        return Response(data)

    def post(self, request):
        serializer = BloodRequestSerializer(data=request.data)
        if serializer.is_valid():
            payload = {k: v for k, v in serializer.validated_data.items()
                    if k not in ('fulfilled', 'created_at')}
            req_doc = BloodRequestDocument(**payload).save()
            return Response(_doc_to_dict(req_doc), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchDonorsAPI(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request, request_id):
        req_doc = BloodRequestDocument.objects(id=request_id).first()
        if not req_doc:
            return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

        pool = [
            {
                'name': d.name, 'blood_group': d.blood_group, 'phone': d.phone,
                'email': d.email, 'location': d.location, 'available': d.available,
            }
            for d in DonorDocument.objects(location__iexact=req_doc.location, available=True)
        ]

        req_obj = BloodRequest(
            hospital=req_doc.hospital, blood_group=req_doc.blood_group,
            location=req_doc.location, units_needed=req_doc.units_needed,
            urgency=req_doc.urgency,
        )

        try:
            matches = MatchEngine(pool).find_matches(req_obj)
        except NoMatchingDonorError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

        sent = notify_matched_donors(matches, {
            'hospital': req_doc.hospital, 'location': req_doc.location,
        })

        req_doc.fulfilled = True
        req_doc.save()

        return Response({
            'matched_count': len(matches),
            'matches': matches,
            'notifications_sent': len(sent),
        }, status=status.HTTP_200_OK)


class CampReportAPI(APIView):
    permission_classes = [AllowAny]


    def get(self, request):
        report = camp_donor_count_report()
        for r in report:
            r['camp_date'] = r['camp_date'].isoformat()
        return Response(report)