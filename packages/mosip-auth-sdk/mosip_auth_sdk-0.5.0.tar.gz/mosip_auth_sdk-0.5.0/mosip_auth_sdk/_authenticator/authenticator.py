import string
import secrets
import logging
import sys
import urllib
from datetime import datetime
from typing import Literal, Optional, Dict, TypeAlias, List
from .auth_models import (
    MOSIPAuthRequest,
    DemographicsModel,
    MOSIPEncryptAuthRequest,
    BiometricModel,
    MOSIPBaseRequest,
    MOSIPOtpRequest,
)
from .utils import CryptoUtility, RestUtility
from .exceptions import AuthenticatorException, Errors, AuthenticatorCryptoException

AuthController: TypeAlias = Literal["kyc", "auth"]


class MOSIPAuthenticator:
    """ """
    def __init__(self, *, config, logger=None):
        """ """
        self._validate_config(config)
        if not logger:
            self.logger = self._init_logger(
                file_path=config.logging.log_file_path,
                level=config.logging.loglevel or logging.INFO,
                format=config.logging.log_format,
            )
        else:
            self.logger = logger

        self.auth_rest_util = RestUtility(
            config.mosip_auth_server.ida_auth_url,
            config.mosip_auth.authorization_header_constant,
            logger=self.logger,
        )
        self.crypto_util = CryptoUtility(
            config.crypto_encrypt, config.crypto_signature, self.logger
        )

        self.auth_domain_scheme = config.mosip_auth_server.ida_auth_domain_uri

        self.partner_misp_lk = str(config.mosip_auth.partner_misp_lk)
        self.partner_id = str(config.mosip_auth.partner_id)
        self.partner_apikey = str(config.mosip_auth.partner_apikey)

        self.ida_auth_version = config.mosip_auth.ida_auth_version
        self.ida_auth_request_id_by_controller: Dict[AuthController, str] = {
            "auth": config.mosip_auth.ida_auth_request_demo_id,
            "kyc": config.mosip_auth.ida_auth_request_kyc_id,
            "otp": config.mosip_auth.ida_auth_request_otp_id,
        }
        self.ida_auth_env = config.mosip_auth.ida_auth_env
        self.timestamp_format = config.mosip_auth.timestamp_format
        self.authorization_header_constant = (
            config.mosip_auth.authorization_header_constant
        )

    def genotp(
            self,
            *,
            individual_id,
            individual_id_type,
            txn_id: Optional[str] = '',
            email: Optional[bool] = False,
            phone: Optional[bool] = False,
    ):
        channels = [
            channel
            for (channel, val) in
            (('email', email), ('phone', phone))
            if val
        ]
        if not channels:
            err_msg = Errors.AUT_OTP_001.value
            self.logger.error(err_msg)
            raise AuthenticatorException(Errors.AUT_OTP_001.name, err_msg)

        request = self._get_default_auth_request(
            'otp',
            individual_id=individual_id,
            id_type=individual_id_type,
            txn_id=txn_id,
        )
        request.otpChannel = channels

        path_params = "/".join(
            map(
                urllib.parse.quote,
                (
                    'otp',
                    self.partner_misp_lk,
                    self.partner_id,
                    self.partner_apikey,
                ),
            )
        )
        full_request_json = request.json()
        self.logger.debug(f"{full_request_json=}")
        try:
            signature_header = {
                "Signature": self.crypto_util.sign_auth_request_data(full_request_json)
            }
        except AuthenticatorCryptoException as exp:
            self.logger.error(
                "Failed to Encrypt Auth Data. Error Message: {}".format(exp)
            )
            raise exp

        self.logger.debug(f'Posting to {path_params}')
        response = self.auth_rest_util.post_request(
            path_params=path_params,
            data=full_request_json,
            additional_headers=signature_header,
        )
        self.logger.info("Auth Request for Demographic Completed.")
        return response

    def auth(
        self,
        *,
        individual_id,
        individual_id_type,
        demographic_data: DemographicsModel,
        otp_value: Optional[str] = "",
        biometrics: Optional[List[BiometricModel]] = [],
        consent=False,
    ):
        return self._authenticate(
            controller="auth",
            individual_id=individual_id,
            individual_id_type=individual_id_type,
            demographic_data=demographic_data,
            otp_value=otp_value,
            biometrics=biometrics,
            consent_obtained=consent,
        )

    def kyc(
        self,
        *,
        individual_id,
        individual_id_type,
        demographic_data: DemographicsModel,
        otp_value: Optional[str] = "",
        biometrics: Optional[List[BiometricModel]] = [],
        consent=False,
    ):
        return self._authenticate(
            controller="kyc",
            individual_id=individual_id,
            individual_id_type=individual_id_type,
            demographic_data=demographic_data,
            otp_value=otp_value,
            biometrics=biometrics,
            consent_obtained=consent,
        )

    def decrypt_response(self, response_body):
        r = response_body.get("response")
        session_key_b64 = r.get("sessionKey")
        identity_b64 = r.get("identity")
        # thumbprint should match the SHA-256 hex of the partner certificate
        # thumbprint = response_body.get('thumbprint')
        decrypted = self.crypto_util.decrypt_auth_data(session_key_b64, identity_b64)
        return decrypted

    @staticmethod
    def _validate_config(config):
        if not config.mosip_auth_server.ida_auth_url:
            raise KeyError(
                "Config should have 'ida_auth_url' set under [mosip_auth_server] section"
            )
        if not config.mosip_auth_server.ida_auth_domain_uri:
            raise KeyError(
                "Config should have 'ida_auth_domain_uri' set under [mosip_auth_server] section"
            )

    @staticmethod
    def _init_logger(*, file_path, format, level):
        logger = logging.getLogger(file_path)
        logger.setLevel(level)
        fileHandler = logging.FileHandler(file_path)
        streamHandler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(format)
        streamHandler.setFormatter(formatter)
        fileHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)
        logger.addHandler(fileHandler)
        return logger

    def _get_default_base_request(
            self,
            controller,
            timestamp,
            txn_id,
    ):
        _timestamp = timestamp or datetime.utcnow()
        timestamp_str = (
            _timestamp.strftime(self.timestamp_format)
            + _timestamp.strftime(".%f")[0:4]
            + "Z"
        )
        transaction_id = txn_id or "".join(
            [secrets.choice(string.digits) for _ in range(10)]
        )
        id = self.ida_auth_request_id_by_controller.get(controller, "")
        if not id:
            err_msg = Errors.AUT_CRY_005.value.format(
                repr(controller),
                " | ".join(self.ida_auth_request_id_by_controller.keys()),
            )
            self.logger.error(f"No id found for {controller}")
            raise AuthenticatorException(Errors.AUT_CRY_005.name, err_msg)
        return MOSIPAuthRequest(
            id=id,
            version=self.ida_auth_version,
            individualId=individual_id,
            individualIdType=id_type,
            transactionID=transaction_id,
            requestTime=timestamp_str,
        )


    def _get_default_auth_request(
        self,
        controller: AuthController,
        *,
        timestamp=None,
        individual_id="",
        txn_id="",
        consent_obtained=False,
        id_type="VID",
    ):
        baserequest = self._get_default_base_request(controller, timestamp, txn_id)
        if controller == 'otp':
            return MOSIPOtpRequest(
                id=baserequest.id,
            	version=baserequest.version,
            	individualId=baserequest.individualId,
            	individualIdType=baserequest.individualIdType,
            	transactionID=baserequest.transactionID,
            	requestTime=baserequest.requestTime,
            )
        return MOSIPAuthRequest(
            ## base request
            id=baserequest.id,
            version=baserequest.version,
            individualId=baserequest.individualId,
            individualIdType=baserequest.individualIdType,
            transactionID=baserequest.transactionID,
            requestTime=baserequest.requestTime,
            ## BaseAuthRequestDto
            specVersion=self.ida_auth_version,
            thumbprint=self.crypto_util.enc_cert_thumbprint,
            domainUri=self.auth_domain_scheme,
            env=self.ida_auth_env,
            ## AuthRequestDto
            request="",
            consentObtained=consent_obtained,
            requestHMAC="",
            requestSessionKey="",
            metadata={},
        )

    def _authenticate(
        self,
        *,
        controller: AuthController,
        individual_id: str,
        demographic_data: DemographicsModel,
        otp_value: Optional[str] = "",
        biometrics: Optional[List[BiometricModel]] = [],
        consent_obtained=False,
        individual_id_type=None,
    ):
        """ """
        self.logger.info("Received Auth Request for demographic.")
        auth_request = self._get_default_auth_request(
            controller,
            individual_id=individual_id,
            consent_obtained=consent_obtained,
            id_type=individual_id_type,
        )
        # auth_request.requestedAuth.demo = True
        # auth_request.requestedAuth.otp = bool(otp_value)
        # auth_request.requestedAuth.bio = bool(biometrics)
        request = MOSIPEncryptAuthRequest(
            timestamp=auth_request.requestTime,
            biometrics=biometrics or [],
            demographics=demographic_data,
            otp=otp_value,
        )

        try:
            (
                auth_request.request,
                auth_request.requestSessionKey,
                auth_request.requestHMAC,
            ) = self.crypto_util.encrypt_auth_data(request.json(exclude_unset=True))
        except AuthenticatorCryptoException as exp:
            self.logger.error(
                "Failed to Encrypt Auth Data. Error Message: {}".format(exp)
            )
            raise exp

        path_params = "/".join(
            map(
                urllib.parse.quote,
                (
                    controller,
                    self.partner_misp_lk,
                    self.partner_id,
                    self.partner_apikey,
                ),
            )
        )
        full_request_json = auth_request.json()
        self.logger.debug(f"{full_request_json=}")
        try:
            signature_header = {
                "Signature": self.crypto_util.sign_auth_request_data(full_request_json)
            }
        except AuthenticatorCryptoException as exp:
            self.logger.error(
                "Failed to Encrypt Auth Data. Error Message: {}".format(exp)
            )
            raise exp

        response = self.auth_rest_util.post_request(
            path_params=path_params,
            data=full_request_json,
            additional_headers=signature_header,
        )
        self.logger.info("Auth Request for Demographic Completed.")
        return response
