from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from bloodtests.models import Test
from bloodtests.serializers import TestSerializer


class BloodTestView(CreateAPIView, RetrieveAPIView):
    """ View for saving and getting Blood test data """

    permission_classes = [AllowAny]
    serializer_class = TestSerializer
    lookup_field = 'code'

    def get_object(self):
        """
        Get blood test by code

        Parameters
        ----------
        code: str,

        Return
        -------
        {code:str, name:str, unit:str, lower:float, upper:float', ideal_range:str} : dict
        """
        code = self.kwargs["code"]
        return get_object_or_404(Test, code=code)

    def get_query_object(self):
        code = self.kwargs["code"]
        return Test.objects.filter(code=code).first()

    def post(self, request, *args, **kwargs):
        """
        Persist blood test

        Parameters
        ----------
        {code:str, name:str, unit:str, lower:float, upper:float', ideal_range:str} : dict

        Return
        -------
        {code:str, name:str, unit:str, lower:float, upper:float', ideal_range:str} : dict
        """
        if self.get_query_object():
            serializer = self.serializer_class(instance=self.get_query_object(),
                                               data=request.data)
        else:
            serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


