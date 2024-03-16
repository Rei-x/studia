import streamlit as st


# if st.session_state.get("counter", 0) < 10:
st.text("Fixed width text")
st.markdown("_Markdown_")  # see #*
st.caption(body="Balloons. Hundreds of them...")
st.latex(r""" e^{i\pi} + 1 = 0 """)
st.write("Most objects")  # df, err, func, keras!
st.write(["st", "is <", 3])  # see *
st.title("My title")
st.header("My header")
st.subheader("My sub")
st.code("for i in range(8): foo()")


# def foo():
#     st.session_state["counter"] = st.session_state.get("counter", 0) + 1
#     st.write("LICZNIK: ", st.session_state.counter)


# st.button("Hit me!", on_click=foo)
