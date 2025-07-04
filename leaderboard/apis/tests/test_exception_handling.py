from django.test import TestCase, RequestFactory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from apis.decorators.exception_handling import handle_api_exceptions

class DummyView(APIView):
    @handle_api_exceptions
    def get(self, request):
        return Response({"ok": True})

    @handle_api_exceptions
    def post(self, request):
        raise ValidationError("Invalid data")

    @handle_api_exceptions
    def put(self, request):
        raise ValueError("Not found")

    @handle_api_exceptions
    def delete(self, request):
        raise Exception("Unexpected error")

class ExceptionHandlingDecoratorTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = DummyView.as_view()

    def test_normal_response(self):
        request = self.factory.get("/dummy/")
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"ok": True})

    def test_validation_error(self):
        request = self.factory.post("/dummy/")
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Validation error")

    def test_value_error(self):
        request = self.factory.put("/dummy/")
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Value error")

    def test_generic_exception(self):
        request = self.factory.delete("/dummy/")
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Internal server error") 