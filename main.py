import time
import streamlit as st
import utils


@st.dialog("Rollback - Are you sure?")
def confirm_rollback():
    st.write("Login to confirm your action:")
    st.subheader(":red[ROLLBACK]")

    username = st.text_input("Username", type="default",  key="username", autocomplete="username")
    password = st.text_input("Password", type="password", key="password", autocomplete="current-password")
    status_box = st.empty()

    if st.button("Confirm"):
        if not utils.check_user(username):
            status_box.error("Invalid user")
            return
        if not utils.check_pw(password):
            status_box.error("Invalid password")
            return

        rollback_url = utils.generate_jenkins_url(utils.JenkinsUrlTypes.ROLLBACK)
        utils.start_jenkins_job(username, rollback_url)
        message = "Successfully submitted Rollback request"
        st.session_state["message"] = message
        status_box.success(message)
        time.sleep(2)
        st.rerun()


@st.dialog("RollForward - Are you sure?")
def confirm_forward():
    st.write("Login to confirm your action:")
    st.subheader(":green[RollForward]")

    username = st.text_input("Username", type="default",  key="username", autocomplete="username")
    password = st.text_input("Password", type="password", key="password", autocomplete="current-password")
    status_box = st.empty()

    if st.button("Confirm"):
        if not utils.check_user(username):
            status_box.error("Invalid user")
            return
        if not utils.check_pw(password):
            status_box.error("Invalid password")
            return

        rollforward_url = utils.generate_jenkins_url(utils.JenkinsUrlTypes.ROLLFORWARD)
        utils.start_jenkins_job(username, rollforward_url)
        message = "Successfully submitted RollForward request"
        st.session_state["message"] = message
        status_box.success(message)
        time.sleep(2)
        st.rerun()

# Actual page
if "message" not in st.session_state:
    st.session_state["message"] = ""


st.set_page_config(
    page_title="PPR Delivery App",
    page_icon=":material/smartphone:",

)
st.title("PPR Delivery App Rollout handler")

col1, col2 = st.columns(2)
message = st.write(st.session_state["message"])

if col1.button("Rollback :material/close:", type="primary"):
    confirm_rollback()

if col2.button(":green-background[RollForward] :material/check:", type="secondary"):
    confirm_forward()
