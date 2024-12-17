from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal


class MOSIPRequestedAuth(BaseModel):
    demo: bool = False
    pin: bool = False
    otp: bool = False
    bio: bool = False


class IdentityInfo(BaseModel):
    language: str
    value: str


class DemographicsModel(BaseModel):
    age: str = ""
    dob: str = ""
    name: List[IdentityInfo] = []
    dobType: List[IdentityInfo] = Field(default_factory=list, alias="dob_type")
    gender: List[IdentityInfo] = Field(default_factory=list)
    phoneNumber: str = Field(default="", alias="phone_number")
    emailId: str = Field(default="", alias="email_id")
    addressLine1: List[IdentityInfo] = Field(
        default_factory=list, alias="address_line1"
    )
    addressLine2: List[IdentityInfo] = Field(
        default_factory=list, alias="address_line2"
    )
    addressLine3: List[IdentityInfo] = Field(
        default_factory=list, alias="address_line3"
    )
    location1: List[IdentityInfo] = Field(default_factory=list)
    location2: List[IdentityInfo] = Field(default_factory=list)
    location3: List[IdentityInfo] = Field(default_factory=list)
    postalCode: str = Field(default="", alias="postal_code")
    fullAddress: List[IdentityInfo] = Field(default_factory=list, alias="full_address")
    metadata: Optional[Dict[str, object]] = None


class MOSIPEncryptAuthRequest(BaseModel):
    biometrics: list
    demographics: DemographicsModel
    otp: str
    timestamp: str


class MOSIPBaseRequest(BaseModel):
    id: str
    version: str
    individualId: str
    individualIdType: str
    transactionID: str
    requestTime: str
class MOSIPOtpRequest(MOSIPBaseRequest):
    otpChannel:  List[Literal['phone', 'email']]
    metadata: dict

class MOSIPAuthRequest(BaseModel):
    id: str
    version: str
    individualId: str
    individualIdType: str
    transactionID: str
    requestTime: str
    specVersion: str
    thumbprint: str
    domainUri: str
    env: str
    requestedAuth: MOSIPRequestedAuth = MOSIPRequestedAuth()
    consentObtained: bool
    requestHMAC: str
    requestSessionKey: str
    request: str
    metadata: dict


class BiometricModelDataDigitalIdField(BaseModel):
    serialNo: str
    make: str
    model: str
    type: str
    deviceSubType: str
    deviceProvider: str
    dp: str
    dpId: str
    deviceProviderId: str
    dateTime: str


class BiometricModelDataField(BaseModel):
    digitalId: BiometricModelDataDigitalIdField
    bioType: str
    bioSubType: str
    bioValue: str
    deviceCode: str
    deviceServiceVersion: str
    transactionId: str
    timestamp: str
    purpose: str
    env: str
    version: str
    domainUri: str
    requestedScore: int
    qualityScore: int


class BiometricModel(BaseModel):
    data: BiometricModelDataField
    hash: str
    sessionKey: str
    specVersion: str
    thumbprint: str
