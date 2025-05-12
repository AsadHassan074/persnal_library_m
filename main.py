import streamlit as st
import pandas as pd
import os

DATA_FILE = "library_data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Title", "Author", "Genre", "Status"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

st.set_page_config(page_title="📖 Personal Library Manager", layout="centered")
st.title("📚 My Personal Library Manager")


df = load_data()

with st.expander("➕ Add a new book"):
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Book Title")
        author = st.text_input("Author")
    with col2:
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Mystery", "Fantasy", "Biography", "Other"])
        status = st.selectbox("Status", ["Want to Read 📌", "Reading 📖", "Read ✅"])

    if st.button("Add Book 📝"):
        if title and author:
            new_book = pd.DataFrame([[title, author, genre, status]], columns=df.columns)
            df = pd.concat([df, new_book], ignore_index=True)
            save_data(df)
            st.success(f"'{title}' by {author} added! ✅")
        else:
            st.warning("Please fill in both Title and Author!")

st.subheader("🔎 My Books")
search = st.text_input("Search by title or author")
filtered_df = df[df["Title"].str.contains(search, case=False, na=False) | df["Author"].str.contains(search, case=False, na=False)]

if not filtered_df.empty:
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.info("No books found. Try adding some!")


with st.expander("🗑️ Delete a Book"):
    if not df.empty:
        to_delete = st.selectbox("Select a book to delete", df["Title"] + " - " + df["Author"])
        if st.button("Delete Book ❌"):
            index = df[df["Title"] + " - " + df["Author"] == to_delete].index
            df.drop(index, inplace=True)
            save_data(df)
            st.success("Book deleted successfully.")
    else:
        st.info("No books available to delete.")

st.markdown("---")
st.markdown("📘 _Your digital bookshelf_ — Made with ❤️ using Streamlit")
