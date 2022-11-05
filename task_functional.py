from api_client import APIClient
import json

USER_DATA_URL = 'https://reqres.in/api/'


def get_users_data():
    client = APIClient(USER_DATA_URL)
    page = 1
    result = []
    while True:
        resp = client.get('users', {'page': page})
        data = json.loads(resp.text)['data']
        if len(data) != 0:
            result += data
            page += 1
        else:
            break
    return result


def prepare_named_sorted(a, b, whole_resp_data):
    result = []
    for _user_data in whole_resp_data:
        if a <= _user_data.get('id') <= b:
            result.append(_user_data.get('first_name') + ' ' + _user_data.get('last_name'))
    return sorted(result)


def get_user_full_name_list(a, b):
    if isinstance(a, int) and isinstance(b, int) and a > 0 and b > 0:
        data = get_users_data()
        return prepare_named_sorted(a, b, data)
    return []


if __name__ == '__main__':
    assert get_user_full_name_list(1, 3) == ['Emma Wong', 'George Bluth', 'Janet Weaver']
    assert get_user_full_name_list(5, 8) == ['Charles Morris', 'Lindsay Ferguson', 'Michael Lawson', 'Tracey Ramos']
    assert get_user_full_name_list(-1, 3) == []
    assert get_user_full_name_list(1, -3) == []
    assert get_user_full_name_list(0, 0) == []
    assert get_user_full_name_list("0", 0) == []
    assert get_user_full_name_list(0, "0") == []

