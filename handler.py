import json

from app.common.auth import token_required
from app.interfaces.api.user_api import  get_user_api, get_all_users_api, create_user_beneficiary_api, get_additional_information_by_id_api, update_foundation_worker_by_id_api, get_clinical_history_by_id_api, update_beneficiary_by_id_api, get_beneficiariesShortInfo_api, delete_additional_information_by_id_api, update_foundation_worker_by_id_api, add_additional_information_by_id_api, get_family_member_user_by_unique_id_api, get_family_group_user_api, create_family_member_user_api, update_family_member_user_api, delete_family_member_user_api, upload_image_s3, get_beneficiary_name_image_api, get_departments_list_api
from app.interfaces.api.login_api import create_login_user_api, login_api, get_name_by_personal_id_api


def get_user(event, context):
    response = token_required(get_user_api)(event, context)
    return response


def get_all_user(event, context):
    response = token_required(get_all_users_api)(event, context)
    return response


def create_user_beneficiary(event, context):
    response = create_user_beneficiary_api(event, context)
    return response


def create_login_user(event, context):
    response = token_required(create_login_user_api)(event, context)
    return response

def create_user(event, context):
    user_data = json.loads(event['body'])
    if user_data['role'] == 'user_beneficiary':
        return create_user_beneficiary(event, context)
    elif user_data['role'] == 'user_worker':
        return create_login_user(event, context)
    else:
        return{
            'statusCode': 400,
            'body': 'Rol no válido'
        }

def login(event, context):
    user_data = json.loads(event['body'])
    response = login_api(user_data)

    status_code = response.status_code
    if response.is_json:
        response_body = response.get_json()
    else:
        # Decodifica response.data si es de tipo bytes
        response_body = response.data.decode('utf-8') if isinstance(response.data, bytes) else response.data

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"

        },
        "body": json.dumps(response_body)
    }

# Handler to get referral cause, support requests and observations of a beneficiary by his id
def get_additional_information_by_id(event, context):
    response = token_required(get_additional_information_by_id_api)(event, context)
    return response

def get_name_by_personal_id(event, context):
    response = get_name_by_personal_id_api(event, context)
    return response

# Handler to update the information of a foundation worker by his id
def update_foundation_worker_by_id(event, context):
    response = token_required(update_foundation_worker_by_id_api)(event, context)
    return response

# Handler to get clinical history by his id
def get_clinical_history_by_id(event, context):
    response = token_required(get_clinical_history_by_id_api)(event, context)
    return response

# Handler to get all beneficiaries parcial information 
def get_beneficiariesShortInfo(event, context):
    response = token_required(get_beneficiariesShortInfo_api)(event, context)
    return response

# Handler to update the information of a beneficary by his id
def update_beneficiary_by_id(event, context):
    response = token_required(update_beneficiary_by_id_api)(event, context)
    return response

# Handler to delete the additional information of a beneficary by his id
def delete_additional_information_by_id(event, context):
    response = token_required(delete_additional_information_by_id_api)(event, context)
    return response

# Handler to add the additional information of a beneficary by his id
def add_additional_information_by_id(event, context):
    response = token_required(add_additional_information_by_id_api)(event, context)
    return response

def get_family_member_user_by_unique_id(event, context):
    response = token_required(get_family_member_user_by_unique_id_api)(event, context)
    return response

def get_family_group_user(event, context):
    response = token_required(get_family_group_user_api)(event, context)
    return response

def create_family_member_user(event, context):
    response = token_required(create_family_member_user_api)(event, context)
    return response

def update_family_member_user(event, context):
    response = token_required(update_family_member_user_api)(event, context)
    return response

def delete_family_member_user(event, context):
    response = token_required(delete_family_member_user_api)(event, context)
    return response

def upload_profile_image(event, context):
    response = token_required(upload_image_s3)(event, context)
    return response

def get_name_and_image_by_personal_id(event, context):
    response = token_required(get_beneficiary_name_image_api)(event, context)
    return response


# aqui empezamos ota vez

def get_departments_list(event, context):
    response = token_required(get_departments_list_api)(event, context)
    return response
