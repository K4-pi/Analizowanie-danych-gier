import streamlit as st

def start():

    st.title("Analizowanie danych gier")
    st.markdown(
        """ 
        Hello World! 
        """
    )

    if st.button("Send balloons!"):
        st.balloons()

if __name__ == "__main__":
  start()