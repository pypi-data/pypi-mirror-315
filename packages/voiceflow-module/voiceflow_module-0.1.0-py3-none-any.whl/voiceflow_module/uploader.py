import requests
import io

def try_upload_text(text_name: str, text: str, token: str, chunk_size: int = 1000, overwrite: bool = True) -> tuple[bool, str]:
    try:
        txt_file = io.BytesIO(text.encode('utf-8-sig'))
        overwrite_param = 'true' if overwrite else 'false'

        url = f'https://api.voiceflow.com/v1/knowledge-base/docs/upload?overwrite={overwrite_param}&maxChunkSize={chunk_size}'
        headers = {
                "accept": "application/json",
                "Authorization": token
            }

        files = {
                "file": (f'{text_name}.txt', txt_file, "text/plain")
            }

        response = requests.post(url, headers=headers, files=files)
        txt_file.close()

        if response.status_code != 200:
            return False, f"Failed to upload '{text_name}' text. {str(response.text)}"
        
        return True, 'Success'
    except Exception as e:
        return False, f"Error while trying to upload '{text_name}' text. {str(e)}"
    

def try_upload_table(table_name: str, items: list, token: str, searchable_fields: list, metadata_fields: list=[], overwrite=True):
    try:
        json_data = {
            "data": {
                "name": table_name,
                "schema": {
                    "searchableFields": searchable_fields,
                    "metadataFields": metadata_fields,
                },
                "items": items
            }
        }
            
        url = "https://api.voiceflow.com/v1/knowledge-base/docs/upload/table"
        if overwrite:
            url += "?overwrite=true"

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": token
        }

        response = requests.post(url, headers=headers, json=json_data)
        if response.status_code != 200:
            return False, f"Failed to upload '{table_name}' text. {str(response.text)}"
        
        return True, 'Success'
    except Exception as e:
        return False, f"Error while trying to upload '{table_name}' text. {str(e)}"