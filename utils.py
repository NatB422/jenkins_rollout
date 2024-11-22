from enum import Enum, auto
import hashlib
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth


def check_user(input_username:str):
    input_hash = hashlib.sha256(input_username.encode()).hexdigest()
    return input_hash == st.secrets["user_hash"]

def check_pw(input_pw:str):
    input_hash = hashlib.sha256(input_pw.encode()).hexdigest()
    return input_hash == st.secrets["pw_hash"]

def start_jenkins_job(username, url):
    basic = HTTPBasicAuth(username, st.secrets["jenkins_token"])

    CRUMB_URL = generate_jenkins_url(JenkinsUrlTypes.CRUMB)
    response = requests.post(CRUMB_URL, auth=basic)
    response.raise_for_status()
    crumb = response.json()["crumb"]

    response = requests.post(url, auth=basic, data={"crumb": crumb})
    response.raise_for_status()
    content = response.content.decode()
    print(content)
    return content


class JenkinsUrlTypes(Enum):
    CRUMB = auto()
    ROLLBACK = auto()
    ROLLFORWARD = auto()


def generate_jenkins_url(url_type:JenkinsUrlTypes):
    JENKINS_HOST = st.secrets["jenkins_host"]

    if url_type == JenkinsUrlTypes.CRUMB:
        return f"{JENKINS_HOST}/crumbIssuer/api/json"

    if url_type == JenkinsUrlTypes.ROLLBACK:
        jobname = st.secrets["rollback_jobname"]
        return f"{JENKINS_HOST}/job/{jobname}/build?delay=0sec"

    if url_type == JenkinsUrlTypes.ROLLFORWARD:
        jobname = st.secrets["rollforward_jobname"]
        return f"{JENKINS_HOST}/job/{jobname}/build?delay=0sec"

    raise Exception("Unrecognised type")
