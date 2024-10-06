# app/infrastructure/database/sql_user_repository.py
import uuid
import psycopg2
import boto3
import base64
from datetime import datetime
import json
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig
from app.common.config import Config
from app.domain.entities.familyMember import FamilyMember
from app.domain.entities.userAccount import UserAccount
from app.domain.repositories.user_repository import UserRepository
from enum import Enum


class Status(Enum):
    OK = 0
    FORBIDDEN = 1
    USER_NOT_FOUND = 2
    DATA_DONT_EXIST = 3
    DATA_TYPE_ERROR = 4
    UNEXPECTED_ERROR = 5

class SqlUserRepository(UserRepository):
    def get_s3_connection(self):
        S3_BUCKET_NAME = Config.S3_BUCKET_NAME
        S3_BASE_URL = Config.S3_BASE_URL
        S3 = boto3.client('s3', aws_access_key_id = Config.S3_ACCESS_KEY_ID, 
                          aws_secret_access_key = Config.S3_ACCESS_KEY)
        return S3, S3_BUCKET_NAME, S3_BASE_URL
    
    def get_db_connection(self):
        return psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASS, host=Config.DB_HOST, port=Config.DB_PORT
        )

    def get_user_by_id(self, user_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user.user_account WHERE personal_id = %s', (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_data:
            return UserAccount(
                id=user_data[0],
                name=user_data[1],
                lastName=user_data[2],
                email=user_data[3],
                active=user_data[4],
                country=user_data[5],
                telephone=user_data[6]
            )
        return None

    def get_all_users(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user.user_account')
        users_data = cursor.fetchall()
        cursor.close()
        conn.close()

        users = []
        for user_data in users_data:
            users.append(UserAccount(
                id=user_data[0],
                name=user_data[1],
                lastName=user_data[2],
                email=user_data[3],
                active=user_data[4],
                country=user_data[5],
                telephone=user_data[6]
            ))

        return users

    def create_user(self, user):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            query1 = '''INSERT INTO "user"."foundation_beneficiary" (
            user_id, personal_id, institution_name,
            identification_type_id, health_entity, interviewed_person, relationship,
            interviewed_person_id, address, district_id, socioeconomic_status_id,
            referred_by, referral_address, referral_phones,
            entity_organization, total_monthly_income,
            referral_cause, support_request, observations, profile_image_link, status_id, creation_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            # cursor.execute('SELECT identification_type_id FROM "user"."identification_type" WHERE description = %s', (user.identification_type_id,))
            # iti = cursor.fetchone()
            #cursor.execute('SELECT district_id FROM "user"."district" WHERE district_name = %s', (user.district_id,))
            #dist = cursor.fetchone()
            # cursor.execute('SELECT socioeconomic_status_id FROM "user"."socioeconomic_status" WHERE socioeconomic_status_value = %s', (user.socioeconomic_status_id,))
            # sei = cursor.fetchone()
            cursor.execute('SELECT status_id FROM "user"."status" WHERE status_name = %s', ("active",))
            status_id = cursor.fetchone()
            values1 = ( str(user.user_id), user.personal_id, user.institution_name, str(user.identification_type_id),
            user.health_entity, user.interviewed_person, user.relationship,
            user.interviewed_person_id, user.address, str(user.district_id), str(user.socioeconomic_status_id), user.referred_by,
            user.referral_address, user.referral_phones,
            user.entity_organization, user.total_monthly_income, user.referral_cause, user.support_request, user.observations, "aquivalaimagen", str(status_id[0]), datetime.now() )
            cursor.execute(query1, values1)
            for person in user.family_members:
                fuuid = uuid.uuid4()
                query2 = 'INSERT INTO "user"."family_member" (family_member_id, personal_id, full_name, age, relationship, education_level, occupation, monthly_income, document_number) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s )'
                
                values2 = (
                    str(fuuid), str(user.personal_id), person['full_name'], person['age'], person['relationship'], person['education_level'],
                    person['occupation'], person['monthly_income'],
                    person['document_number']
                )
                cursor.execute(query2, values2)
            housing = user.housing_type
            huuid = uuid.uuid4()
            query3 = 'INSERT INTO "user"."housing_type" (housing_type_id, personal_id, description, rental_value_month, loan_value_month, bank) VALUES ( %s, %s, %s, %s, %s, %s )'
            values3 = (
                str(huuid), str(user.personal_id), housing['description'], housing['rental_value_month'], housing['loan_value_month'], housing['bank']
            )
            cursor.execute(query3, values3)
            conn.commit()
        except psycopg2.Error as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
        return user

    # SQL repository to get referral cause, support requests and observations of a beneficiary by his id
    def get_additional_information_by_id(self, personal_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT personal_id, referral_cause, support_request, observations FROM "user"."foundation_beneficiary" WHERE personal_id = %s', (personal_id,))
            user_data = cursor.fetchone()
        except:
            user_data = False
        cursor.close()
        conn.close()
        if user_data:
            return {
                'personal_id': user_data[0],
                'referral_cause': user_data[1],
                'support_request': user_data[2],
                'observations': user_data[3]}
        return None

    # SQL repository to update the information of a foundation worker by his id
    def update_foundation_worker_by_id(self, worker_id, data):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            valores = ", ".join([str(key) + " = %s" for key in data])
            query = 'UPDATE "user"."foundation_worker" SET ' + valores + " WHERE worker_id = %s"
            cursor.execute(query, list(data.values()) + [worker_id])
            conn.commit()
            flag = True
        except:
            flag = False
        cursor.close()
        conn.close()
        return flag
    
    # SQL repository to get the clinical history of a user by their personal ID
    def get_clinical_history_by_id(self, user_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT user_id, clinical_history_number, health_entity, interviewed_person, interviewed_person_id, observations FROM "user"."foundation_beneficiary" WHERE user_id = %s', (user_id,))
            user_data = cursor.fetchone()
        except:
            user_data = False
        cursor.close()
        conn.close()
        if user_data:
            return {
                'user_id': user_data[0],
                'interviewed_person_id': user_data[4],
                'interviewed_person': user_data[3],
                'clinical history number': user_data[1],
                'health_entity': user_data[2],
                'observations': user_data[5]}
        return None
    
    # SQL repository to get all beneficiaries parcial information 
    def get_beneficiariesShortInfo(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT personal_id, full_name, profile_image_link FROM "user"."foundation_beneficiary" INNER JOIN "user"."family_member" USING (personal_id)')
            user_data = cursor.fetchall()
        except:
            user_data = False
        cursor.close()
        conn.close()
        if user_data:
            beneficiaries_information = []
            for row in user_data:
                beneficiaries_information.append({
                    'Personal ID': row[0],
                    'Full Name': row[1],
                    "Image Link": row[2]})
            return beneficiaries_information
        return None

    # SQL repository to update the information of a beneficiary by his id
    def update_beneficiary_by_id(self, data):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        # Manage when selected data cannot be modified
        if "user_id" in data or "identification_type_id" in data or "creation_date" in data:
            flag = Status.FORBIDDEN
        else:
            try:
                personal_id = data["personal_id"]
                del data["personal_id"]
                valores = ", ".join([str(key) + " = %s" for key in data])
                query = 'UPDATE "user"."foundation_beneficiary" SET ' + valores + " WHERE personal_id = %s"
                cursor.execute(query, list(data.values()) + [personal_id])
                conn.commit()
                # Manage when no user found with the specified id
                flag = (Status.OK if cursor.rowcount else Status.USER_NOT_FOUND)
            # Manage when the data you want to modify does not exist 
            except psycopg2.ProgrammingError:
                flag = Status.DATA_DONT_EXIST
            # Manage when data format is invalid
            except psycopg2.errors.InvalidTextRepresentation:
                flag = Status.DATA_TYPE_ERROR
            # Manage any other errors
            except:
                flag = Status.UNEXPECTED_ERROR
        cursor.close()
        conn.close()
        return flag
    
    # SQL repository to delete the additional information of a beneficiary by his id
    def delete_additional_information_by_id(self, personal_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE "user"."foundation_beneficiary" SET referral_cause = NULL, support_request = NULL, observations = NULL WHERE personal_id = %s', (personal_id,))
            conn.commit()
            # Manage when no user found with the specified id
            flag = (Status.OK if cursor.rowcount else Status.USER_NOT_FOUND)
        # Manage when the data you want to modify does not exist 
        except psycopg2.ProgrammingError:
            flag = Status.DATA_DONT_EXIST
        # Manage any other errors
        except:
            flag = Status.UNEXPECTED_ERROR
        cursor.close()
        conn.close()
        return flag


    # SQL repository to add the additional information of a beneficiary by his id
    def add_additional_information_by_id(self, data):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            columnas = [data[key] for key in data if key != 'personal_id'] + [data['personal_id']]
            valores = ", ".join([str(key) + " = %s" for key in data if key != 'personal_id'])
            query = 'UPDATE "user"."foundation_beneficiary" SET ' + valores + " WHERE personal_id = %s"
            cursor.execute(query, columnas)
            conn.commit()
            # Manage when no user found with the specified id
            flag = (Status.OK if cursor.rowcount else Status.USER_NOT_FOUND)
        # Manage when the data you want to modify does not exist 
        except psycopg2.ProgrammingError:
            flag = Status.DATA_DONT_EXIST
        # Manage when data format is invalid
        except psycopg2.errors.InvalidTextRepresentation:
            flag = Status.DATA_TYPE_ERROR
        # Manage any other errors
        except:
            flag = Status.UNEXPECTED_ERROR
        cursor.close()
        conn.close()
        return flag

    # SQL repository to get the family member information by his unique id
    def get_family_member_user_by_unique_id(self, family_member_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "user"."family_member" WHERE family_member_id = %s', (family_member_id,))

        family_member_data = cursor.fetchone()

        cursor.close()
        conn.close()

        member = None
        if family_member_data:
            member = FamilyMember(family_member_data[0], family_member_data[1], family_member_data[2], family_member_data[3], family_member_data[4], family_member_data[5], family_member_data[6], family_member_data[7])

        return member

    def get_family_group_user(self, personal_id):
        response = None

        conn = self.get_db_connection()
        cursor = conn.cursor()

        query = '''
        SELECT se.socioeconomic_status_value
        FROM "user"."foundation_beneficiary" AS b
        JOIN "user"."socioeconomic_status" AS se ON b.socioeconomic_status_id = se.socioeconomic_status_id
        WHERE b.personal_id = %s
        '''
        cursor.execute(query, (personal_id,))
        socioeconomic_status_data = cursor.fetchone()

        cursor.execute('SELECT * FROM "user"."family_member" WHERE personal_id = %s', (personal_id,))
        family_members_data = cursor.fetchall()

        cursor.close()
        conn.close()

        members = None
        if family_members_data:
            members = [FamilyMember(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]) for data in family_members_data]

        if socioeconomic_status_data:
            response = {
                "socioeconomic_status": socioeconomic_status_data[0],
                "family_group": members
            }

        return response

    def create_family_member_user(self, family_member):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        new_id = str(uuid.uuid4())
        family_member['family_member_id'] = new_id

        if 'personal_id' not in family_member:
            flag = Status.FORBIDDEN
        else:
            try:
                query = '''
                    INSERT INTO "user"."family_member" 
                    (family_member_id, personal_id, full_name, age, relationship, education_level, occupation, monthly_income)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                '''
                cursor.execute(query, (
                    family_member['family_member_id'],
                    family_member['personal_id'],
                    family_member['full_name'],
                    family_member['age'],
                    family_member['relationship'],
                    family_member['education_level'],
                    family_member['occupation'],
                    family_member['monthly_income']
                ))
                conn.commit()
                # Manage when no user found with the specified id
                flag = (Status.OK if cursor.rowcount else Status.USER_NOT_FOUND)
            except psycopg2.ProgrammingError:
                flag = Status.DATA_DONT_EXIST
            except psycopg2.errors.InvalidTextRepresentation:
                flag = Status.DATA_TYPE_ERROR
            except:
                flag = Status.UNEXPECTED_ERROR

        cursor.close()
        conn.close()

        return flag

    def update_family_member_user(self, family_member):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        if "family_member_id" not in family_member:
            flag = Status.FORBIDDEN
        else:
            try:
                columns = ", ".join([str(key) + " = %s" for key in family_member if key != 'family_member_id'])
                values = [family_member[key] for key in family_member if key != 'family_member_id'] + [family_member['family_member_id']]


                query = 'UPDATE "user"."family_member" SET ' + columns + ' WHERE family_member_id = %s'
                cursor.execute(query, values)
                conn.commit()

                flag = (Status.OK if cursor.rowcount else Status.USER_NOT_FOUND)
            except psycopg2.ProgrammingError:
                flag = Status.DATA_DONT_EXIST
            except psycopg2.errors.InvalidTextRepresentation:
                flag = Status.DATA_TYPE_ERROR
            except:
                flag = Status.UNEXPECTED_ERROR
        cursor.close()
        conn.close()

        return flag


    def delete_family_member_user(self, family_member_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        try:
            query = 'DELETE FROM "user"."family_member" WHERE family_member_id = %s'
            cursor.execute(query, (family_member_id, ))
            conn.commit()
            # Manage when no user found with the specified id
            flag = (Status.OK if cursor.rowcount else Status.USER_NOT_FOUND)
        except psycopg2.ProgrammingError:
            flag = Status.DATA_DONT_EXIST
        except psycopg2.errors.InvalidTextRepresentation:
            flag = Status.DATA_TYPE_ERROR
        except:
            flag = Status.UNEXPECTED_ERROR

        cursor.close()
        conn.close()
        return flag


    
    def upload_image_s3(self, personal_id, file_extension, file):
        S3, BUCKET_NAME, BUCKET_URL = self.get_s3_connection()
        conn = self.get_db_connection()
        cursor = conn.cursor()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        url = f"{personal_id}/profile_image/{unique_filename}"
        success = True
        try:
            try:
                S3.head_object(Bucket=BUCKET_NAME, Key=f"{personal_id}/profile_image/")
            except ClientError as e:
                if e.response['Error']['Code'] == '404':
                    S3.put_object(Bucket=BUCKET_NAME, Key=f"{personal_id}/profile_image/", Body='')
            content = S3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{personal_id}/profile_image/")
            if 'Contents' in content:
                for obj in content['Contents']:
                    tmp = obj['Key']
                    S3.delete_object(Bucket=BUCKET_NAME, Key=f"{tmp}")
            imagen_bytes = base64.b64decode(file.split(',')[1])
            S3.put_object(Bucket=BUCKET_NAME, Key = url, Body = imagen_bytes)
            cursor.execute("""UPDATE "user"."foundation_beneficiary" SET profile_image_link = %s WHERE personal_id = %s""", (url, personal_id,))
            conn.commit()
        except (ClientError, psycopg2.Error) as e:
            if isinstance(e, psycopg2.Error): 
                conn.rollback()
            success = False 
            raise e
        finally:
            cursor.close()
            conn.close()
            S3.close()
        if success == True:
            return { "statusCode" : 202 }
        else: return { "statusCode" : 500 }
    
    def get_beneficiary_name_image(self, personal_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT full_name, profile_image_link FROM "user"."foundation_beneficiary" INNER JOIN "user"."family_member" USING (personal_id)', (personal_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        if user_data:
            return {
                'full_name': user_data[0],
                'profile_image_link': user_data[1]}
        return None