import textwrap
import streamlit as st


class CareBotView:

    def __init__(self):
        self.__is_ui = self.is_streamlit()
        self.initialize_ui()

    def get_is_ui(self) -> bool:
        """
        Returns the self.__is_ui variable of the view

        Returns:
            bool: The self.__is_ui variable.
        """
        return self.__is_ui

    @staticmethod
    def render_sidebar(logo_path: str) -> None:
        """
        Renders the sidebar in the Streamlit app with a logo from a local path
        and extended introductory text.

        Parameters: - logo_path (str): The local file path to the logo image to
        be displayed in the sidebar.

        The sidebar includes: - A logo centered at the top. - Detailed
        introductory text about the capabilities of Care-Bot, including
        listening for keywords and providing assistance.
        """

        # Display the image from a local path
        st.sidebar.image(logo_path, width=250,
                         caption="Care-Bot, your personal assistant 🤖")

        # Add the updated introductory text
        st.sidebar.markdown(
            """
            <hr style='border: none; border-top: 1px solid #ccc; margin:
             20px 0px;'>
            <p style='text-align: center; font-size: 16px;'>
                Hi there! I'm <strong>Care-Bot</strong>, your personal
                assistant 🤖.
            </p>
            <p style='text-align: center; font-size: 16px;'>
                I'm here to help you by listening for keywords and situations
                where you may require assistance.
            </p>
            <p style='text-align: center; font-size: 16px;'>
                You can talk to me at any time using my name
                 <strong>Care-Bot</strong>.
            </p>
            <p style='text-align: center; font-size: 16px;'>
                I'm always listening and ready to assist you with your needs.
            </p>
            """,
            unsafe_allow_html=True,
        )

    def display_streamlit_message(self, message_text: str,
                                  is_user: bool = True) -> None:
        """
        Displays a message in the Streamlit app, with styling based on the
        message sender.

        Parameters: - message_text (str): The text of the message to be
        displayed. - is_user (bool, optional): Flag indicating whether the
        message is from the user (True) or the bot (False). Defaults to True.

        The function styles the message differently based on the sender: -
        User messages are displayed with a blue background and white text. -
        Bot messages are displayed with a light blue background and black text.

        Messages are wrapped to ensure a consistent and readable format,
        and each message is stored as a placeholder in the Streamlit session
        state for potential later removal.
        """
        if not self.get_is_ui():
            return

        color = "blue" if is_user else "#ADD8E6"
        text_color = "white" if is_user else "black"

        wrapped_text = textwrap.fill(message_text,
                                     width=70 if is_user else 90)
        message_html = "\n".join(
            [f"<div style='text-align: left;'>{line}</div>" for line in
             wrapped_text.splitlines()])

        message_display = st.markdown(
            f"<div style='padding: 10px;'>"
            f"<div style='background-color: {color}; padding: 10px; "
            f"border-radius: 5px; color: {text_color}; text-align: left;'>"
            f"{message_html}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        # Store the placeholder in the session state for later removal
        st.session_state['message_placeholders'].append(message_display)

    def clear_streamlit(self) -> None:
        """
        Use Streamlit rerun to refresh the app.
        """
        if not self.get_is_ui():
            return

        st.rerun()

    def clear_streamlit_messages(self) -> None:
        """
        Clears all messages displayed by the display_streamlit_message
        function.
        """
        if not self.get_is_ui():
            return

        while st.session_state['message_placeholders']:
            message_placeholder = st.session_state[
                'message_placeholders'].pop()
            message_placeholder.empty()  # Clear the placeholder

    @staticmethod
    def is_streamlit() -> bool:
        """
        Function to check whether python code is run within streamlit

        Returns
        -------
        use_streamlit : boolean
            True if code is run within streamlit, else False
        """
        try:
            from streamlit.runtime.scriptrunner import get_script_run_ctx
            if not get_script_run_ctx():
                use_streamlit = False
            else:
                use_streamlit = True
        except ModuleNotFoundError:
            use_streamlit = False
        return use_streamlit

    def initialize_ui(self) -> None:
        """
        Initializes the UI components if the UI mode is enabled.
        """
        if self.get_is_ui():
            logo = "Images/logo.jpg"
            self.render_sidebar(logo)
            st.title("🤖 Care-Bot AI")
            st.markdown("<style>body {font-size: 18px;}</style>",
                        unsafe_allow_html=True)
            st.text("🤖 Listening...")

            if 'message_placeholders' not in st.session_state:
                st.session_state['message_placeholders'] = []
