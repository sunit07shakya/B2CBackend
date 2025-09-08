from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from accounts.models import Address, Company
from accounts.serializers.address_serializer import AddressSerializer


class AddressListCreateView(APIView):
    """List all addresses or add a new one"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # If user is a seller → include company addresses too
        if hasattr(request.user, "company"):
            addresses = Address.objects.filter(company=request.user.company)
        else:
            addresses = Address.objects.filter(user=request.user)

        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            if hasattr(request.user, "company") and request.data.get("for_company"):
                serializer.save(company=request.user.company)
            else:
                serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressUpdateDeleteView(APIView):
    """Update or delete an address"""

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            # Check ownership (user or company)
            if hasattr(request.user, "company"):
                address = Address.objects.get(id=pk, company=request.user.company)
            else:
                address = Address.objects.get(id=pk, user=request.user)
        except Address.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            if hasattr(request.user, "company"):
                address = Address.objects.get(id=pk, company=request.user.company)
            else:
                address = Address.objects.get(id=pk, user=request.user)
        except Address.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

        address.delete()
        return Response({"message": "Address deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
