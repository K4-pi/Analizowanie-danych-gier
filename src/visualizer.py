import streamlit as st

def start():
    print("visualizer")

    st.title("Analizowanie danych gier")
    st.markdown(
        """ 
        Hello World! 
        """
    )

    if st.button("Send balloons!"):
        st.balloons()