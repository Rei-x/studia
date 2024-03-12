import streamlit as st

st.text("Fixed width text")
st.markdown("_Markdown_")  # see #*
st.caption("Balloons. Hundreds of them...")
st.latex(r""" e^{i\pi} + 1 = 0 """)
st.write("Most objects")  # df, err, func, keras!
st.write(["st", "is <", 3])  # see *
st.title("My title")
st.header("My header")
st.subheader("My sub")
st.code("for i in range(8): foo()")


def foo():
    st.write("foo")


st.button("Hit me!", on_click=foo)

# * optional kwarg unsafe_allow_html = True
