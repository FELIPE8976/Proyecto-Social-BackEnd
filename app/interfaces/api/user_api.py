# app/interfaces/api/user_api.py
import json
import base64
from flask import Flask, abort
from app.infrastructure.database.sql_user_repository import SqlUserRepository, Status
from app.domain.services.user_service import UserService
from app.common.auth import token_required

app = Flask(__name__)

@token_required
def get_user_api(event, context):
    user_id = event['pathParameters']['id']
    with app.app_context():
        user_repository = SqlUserRepository()
        user_service = UserService(user_repository)
        user = user_service.get_user(user_id)

        if user is None:
            return {
                "statusCode": 404,
                "body": "User not found",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

        return {
            "statusCode": 200,
            "body": json.dumps(user.to_dict()),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }


@token_required
def get_all_users_api(event, context):
    with app.app_context():
        user_repository = SqlUserRepository()
        user_service = UserService(user_repository)
        users = user_service.get_all_users()

        users_list = []
        for user in users:
            users_list.append({
                "id": user.id,
                "name": user.name,
                "lastName": user.lastName,
                "email": user.email,
                "active": user.active,
                "country": user.country,
                "telephone": user.telephone
            })

        return {
        "statusCode": 200,
        "body": json.dumps(users_list),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
    }


@token_required
def create_user_api(event, context):

    with app.app_context():
        try:
            data = json.loads(event['body'])
            user_repository = SqlUserRepository()
            user_service = UserService(user_repository)
            user = user_service.create_user(data['name'], data['lastName'], data['email'],data['active'], data['country'], data['telephone'])
            user_dict = user.to_dict()
            return {
                "statusCode": 201,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(user_dict)
            }
        except Exception as e:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"message": str(e)})
            }

@token_required
def create_user_beneficiary_api(event, context):

    with app.app_context():
        try:
            data = json.loads(event['body'])
            user_repository = SqlUserRepository()
            user_service = UserService(user_repository)
            user = user_service.create_user(data['personal_id'], data['institution_name'],
                data['identification_type_id'], data['health_entity'], data['interviewed_person'], data['relationship'],
                data['interviewed_person_id'], data['address'], data['district_id'], data['socioeconomic_status_id'], data['housing_type'],
                data['referred_by'], data['referral_address'], data['referral_phones'],data['entity_organization'], data['family_members'],
                data['total_monthly_income'], data['referral_cause'], data['support_request'], data['observations'])
            return {
                "statusCode": 201,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(data)
            }
        except Exception as e:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"message": str(e)})
            }


# API to get referral cause, support requests and observations of a beneficiary by his id
@token_required
def get_additional_information_by_id_api(event, context):
    user_id = event['pathParameters']['id']
    with app.app_context():
        user_repository = SqlUserRepository()
        user_service = UserService(user_repository)
        user = user_service.get_additional_information_by_id(user_id)

        if user is None:
            return {
                "statusCode": 404,
                "body": "User not found",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

        return {
            "statusCode": 200,
            "body": json.dumps(user),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }
    
# API to update the information of a foundation worker by his id
@token_required
def update_foundation_worker_by_id_api(event, context):
    worker_id = event['pathParameters']['id']
    data = json.loads(event['body'])
    with app.app_context():
        user_repository = SqlUserRepository()
        user_service = UserService(user_repository)
        flag = user_service.update_foundation_worker_by_id(worker_id, data)
        return {
            "statusCode": (200 if flag else 404),
            "body": ("Foundation worker updated successfully" if flag else "User not found"),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }
    
# API to get the clinical history of a user by their personal ID
@token_required
def get_clinical_history_by_id_api(event, context):
    user_id = event['pathParameters']['id']
    with app.app_context():
        user_repository = SqlUserRepository()
        user_service = UserService(user_repository)
        user = user_service.get_clinical_history_by_id(user_id)

        if user is None:
            return {
                "statusCode": 404,
                "body": "User not found",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        return {
            "statusCode": 200,
            "body": json.dumps(user),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }
    
# API to get all beneficiaries parcial information 
@token_required
def get_beneficiariesShortInfo_api(event, context):
    with app.app_context():
        user_repository = SqlUserRepository()
        user_service = UserService(user_repository)
        user = user_service.get_beneficiariesShortInfo()
        if user is None:
            return {
                "statusCode": 404,
                "body": "User not found",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        return {
            "statusCode": 200,
            "body": json.dumps(user),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

# API to update the information of a beneficiary by his id
@token_required
def update_beneficiary_by_id_api(event, context):
    # The data you want to modify must be a subset of the columns in the foundation_beneficiary table
    # The data received must be in the following format: {"column1": "value1",..., "column2": "value2"}
    data = json.loads(event['body'])
    with app.app_context():
        user_repository = SqlUserRepository()
        user_service = UserService(user_repository)
        flag = user_service.update_beneficiary_by_id(data)
        if flag.name == "OK":
            return {
                "statusCode": 200,
                "body": "Beneficiary updated successfully",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }      
        elif flag.name == "FORBIDDEN":
            return {
                "statusCode": 403,
                "body": "Cannot modify selected data",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        elif flag.name == "USER_NOT_FOUND":
            return {
                "statusCode": 404,
                "body": "Beneficiary not found",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        elif flag.name == "DATA_DONT_EXIST":
            return {
                "statusCode": 404,
                "body": "The data you want to modify does not exist in the table",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        elif flag.name == "DATA_TYPE_ERROR":
            return {
                "statusCode": 422,
                "body": "Invalid data types",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        elif flag.name == "UNEXPECTED_ERROR":
            return {
                "statusCode": 500,
                "body": "Unexpected error",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        
# API to delete the additional information of a beneficiary by his id
@token_required
def delete_additional_information_by_id_api(event, context):
    personal_id = event['pathParameters']['id']
    with app.app_context():
        user_repository = SqlUserRepository()
        user_service = UserService(user_repository)
        flag = user_service.delete_additional_information_by_id(personal_id)
        if flag.name == "OK":
            return {
                "statusCode": 200,
                "body": "Additional Information Deleted Successfully",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }      
        elif flag.name == "USER_NOT_FOUND":
            return {
                "statusCode": 404,
                "body": "Beneficiary not found",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        elif flag.name == "DATA_DONT_EXIST":
            return {
                "statusCode": 404,
                "body": "The data you want to modify does not exist in the table or it's not part of the additional beneficiary information.",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        elif flag.name == "UNEXPECTED_ERROR":
            return {
                "statusCode": 500,
                "body": "Unexpected error",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

# API to add the information of a beneficiary by his id
@token_required
def add_additional_information_by_id_api(event, context):
    # The data you want to modify must be a subset of the columns in the foundation_beneficiary table
    # The data received must be in the following format: {"column1": "value1",..., "column2": "value2"}
    data = json.loads(event['body'])
    with app.app_context():
        user_repository = SqlUserRepository()
        user_service = UserService(user_repository)
        flag = user_service.add_additional_information_by_id(data)
        if flag.name == "OK":
            return {
                "statusCode": 200,
                "body": "Additional Information Added successfully",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }      
        elif flag.name == "USER_NOT_FOUND":
            return {
                "statusCode": 404,
                "body": "Beneficiary not found",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        elif flag.name == "DATA_DONT_EXIST":
            return {
                "statusCode": 404,
                "body": "The data you want to add does not exist in the table",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        elif flag.name == "DATA_TYPE_ERROR":
            return {
                "statusCode": 422,
                "body": "Invalid data types",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        elif flag.name == "UNEXPECTED_ERROR":
            return {
                "statusCode": 500,
                "body": "Unexpected error",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

# API to get the family member information by his unique id
@token_required
def get_family_member_user_by_unique_id_api(event, context):
    family_member_id = event['pathParameters']['id']
    with app.app_context():
        user_repository = SqlUserRepository()
        user_service = UserService(user_repository)
        family_member = user_service.get_family_member_user_by_unique_id(family_member_id)
        if family_member is None:
            return {
                "statusCode": 404,
                "body": "Family member not found",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        return {
            "statusCode": 200,
            "body": json.dumps(family_member.to_dict()),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

@token_required
def get_family_group_user_api(event, context):
    personal_id = event['pathParameters']['id']

    with app.app_context():
        user_repository = SqlUserRepository()
        user_service = UserService(user_repository)
        data = user_service.get_family_group_user(personal_id)
        response = {
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "statusCode": 200
        }

        if data:
            members = [member.to_dict() for member in data['family_group']]
            format_body = {
                "socioeconomic_status": data['socioeconomic_status'],
                "family_members": members
            }

            response["statusCode"] = 200
            response["body"] = json.dumps(format_body)
        else:
            response["statusCode"]= 404
            response["body"] = "Cannot found family members for that personal_id"

        return response

@token_required
def create_family_member_user_api(event, context):
    family_member = json.loads(event['body'])
    with app.app_context():

        user_repository = SqlUserRepository()
        user_service = UserService(user_repository)
        flag = user_service.create_family_member_user(family_member)

        response = {
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "statusCode": 200
        }
        if flag.name == "OK":
            response["statusCode"] = 200
            response["body"] = "Family member created successfully"
        elif flag.name == "FORBIDDEN":
            response["statusCode"] = 403
            response["body"] = "Cannot create family member"
        elif flag.name == "USER_NOT_FOUND":
            response["statusCode"] = 404
            response["body"] = "Family member not found"
        elif flag.name == "DATA_DONT_EXIST":
            response["statusCode"] = 404
            response["body"] = "Cannot create data in the table family member"
        elif flag.name == "DATA_TYPE_ERROR":
            response["statusCode"] = 422
            response["body"] = "Invalid data types"
        elif flag.name == "UNEXPECTED_ERROR":
            response["statusCode"] = 500
            response["body"] = "Unexpected Error"

        return response

@token_required
def update_family_member_user_api(event, context):
    family_member = json.loads(event['body'])

    with app.app_context():
        user_repository = SqlUserRepository()
        user_service = UserService(user_repository)
        flag = user_service.update_family_member_user(family_member)
        response = {
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "statusCode": 200
        }
        if flag.name == "OK":
            response["statusCode"] = 200
            response["body"] = "Family member updated successfully"
        elif flag.name == "FORBIDDEN":
            response["statusCode"] = 403
            response["body"] = "Cannot modify selected data"
        elif flag.name == "USER_NOT_FOUND":
            response["statusCode"] = 404
            response["body"] = "Family member not found"
        elif flag.name == "DATA_DONT_EXIST":
            response["statusCode"] = 404
            response["body"] = "The data you want to modify does not exist in the table"
        elif flag.name == "DATA_TYPE_ERROR":
            response["statusCode"] = 422
            response["body"] = "Invalid data types"
        elif flag.name == "UNEXPECTED_ERROR":
            response["statusCode"] = 500
            response["body"] = "Unexpected Error"

        return response

@token_required
def delete_family_member_user_api(event, context):
    family_member_id = event['pathParameters']['id']
    with app.app_context():

        user_repository = SqlUserRepository()
        user_service = UserService(user_repository)
        flag = user_service.delete_family_member_user(family_member_id)

        response = {
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "statusCode": 200
        }

        if flag.name == "OK":
            response["statusCode"] = 200
            response["body"] = "Family member deleted successfully"
        elif flag.name == "FORBIDDEN":
            response["statusCode"] = 403
            response["body"] = "Cannot delete current family member"
        elif flag.name == "USER_NOT_FOUND":
            response["statusCode"] = 404
            response["body"] = "Family member id not found"
        elif flag.name == "DATA_DONT_EXIST":
            response["statusCode"] = 404
            response["body"] = "The data you want to delete does not exist in the table"
        elif flag.name == "DATA_TYPE_ERROR":
            response["statusCode"] = 422
            response["body"] = "Invalid data types"
        elif flag.name == "UNEXPECTED_ERROR":
            response["statusCode"] = 500
            response["body"] = "Unexpected Error"

        return response

def upload_image_s3(event, context):
    data = json.loads(event['body'])
    personal_id, extension_file, file = data['personal_id'], data['file'], data['image']
    allowed_image_headers = ['PNG', 'JPG', 'PDF', 'DOCX']
    if not extension_file.upper() in allowed_image_headers:
        return {
                "statusCode": 404,
                "body": "File type not allowed",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
    try:
        user_repository = SqlUserRepository()
        user_service = UserService(user_repository)
        response = user_service.upload_image_s3(personal_id, extension_file, file)
        return response
    except Exception as e:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"message": str(e)})
            }
    
def get_beneficiary_name_image_api(event, context):
    personal_id = event['pathParameters']['id']
    with app.app_context():
        user_repository = SqlUserRepository()
        user_service = UserService(user_repository)
        user = user_service.get_beneficiary_name_image(personal_id)
        if user is None:
            return {
                "statusCode": 404,
                "body": "Beneficiary not found",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        return {
            "statusCode": 200,
            "body": json.dumps(user),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }
    

@token_required
def get_departments_list_api( event, context):
    with app.app_context():
        user_repository = SqlUserRepository()
        user_service = UserService(user_repository)
        departments = user_service.get_all_departments()

        departments_list = []
        for department in departments:
            departments_list.append({
                "department_id": department.department_id,
                "name": department.name,
            })

        return {
        "statusCode": 200,
        "body": json.dumps(departments_list),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
    }
