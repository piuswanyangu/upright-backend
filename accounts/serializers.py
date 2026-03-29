from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add custom claims to the response dictionary
        data['role'] = self.user.role
        
        # If the user is a professional, add their specific profession role (e.g., LAWYER or COUNSELOR)
        if hasattr(self.user, 'professional_profile'):
            data['profession_role'] = self.user.professional_profile.role
            
        return data
