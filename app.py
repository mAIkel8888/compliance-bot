import streamlit as st
from controllers.user_controller import create_user, authenticate_user
from controllers.category_controller import create_category, get_categories
from controllers.product_controller import create_product, get_products
from controllers.shopping_list_controller import create_shopping_list, get_shopping_lists, add_item_to_list, get_list_items, get_shopping_list_by_id
from controllers.stock_controller import add_to_stock, get_stock, remove_from_stock

def main():
    st.title("Lista de Compras")

    if 'user' not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        st.write(f"Bem-vindo, {st.session_state.user['username']}!")
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()

        st.header("Categorias")
        category_name = st.text_input("Nova Categoria")
        if st.button("Adicionar Categoria"):
            if create_category(category_name):
                st.success("Categoria adicionada com sucesso!")
            else:
                st.error("Erro ao adicionar categoria.")

        st.header("Produtos")
        product_name = st.text_input("Novo Produto")
        categories = get_categories()
        category_id = st.selectbox("Categoria", [c['id'] for c in categories], format_func=lambda x: [c['name'] for c in categories if c['id'] == x][0])
        if st.button("Adicionar Produto"):
            if create_product(product_name, category_id):
                st.success("Produto adicionado com sucesso!")
            else:
                st.error("Erro ao adicionar produto.")

        st.header("Minhas Listas de Compras")

        st.subheader("Criar Nova Lista")
        list_name = st.text_input("Nome da Nova Lista")
        if st.button("Criar"):
            list_id = create_shopping_list(list_name, st.session_state.user['id'])
            if list_id:
                st.success(f"Lista '{list_name}' criada com sucesso!")
            else:
                st.error("Erro ao criar lista.")

        st.subheader("Importar Lista")
        shared_link = st.text_input("Link da Lista Compartilhada")
        if st.button("Importar"):
            try:
                shared_list_id = int(shared_link.split("=")[-1])
                shared_list = get_shopping_list_by_id(shared_list_id)
                if shared_list:
                    new_list_id = create_shopping_list(f"Importada - {shared_list['name']}", st.session_state.user['id'])
                    if new_list_id:
                        items = get_list_items(shared_list_id)
                        for item in items:
                            add_item_to_list(new_list_id, item['product_id'], item['quantity'])
                        st.success("Lista importada com sucesso!")
                    else:
                        st.error("Erro ao importar lista.")
                else:
                    st.error("Lista compartilhada não encontrada.")
            except:
                st.error("Link inválido.")

        shopping_lists = get_shopping_lists(st.session_state.user['id'])
        selected_list_id = st.selectbox("Selecione uma lista", [l['id'] for l in shopping_lists], format_func=lambda x: [l['name'] for l in shopping_lists if l['id'] == x][0])

        if selected_list_id:
            st.header(f"Itens da Lista")

            share_url = f"http://localhost:8501/?list_id={selected_list_id}"
            st.write(f"Link para compartilhar: `{share_url}`")

            products = get_products()
            product_id = st.selectbox("Produto", [p['id'] for p in products], format_func=lambda x: [p['name'] for p in products if p['id'] == x][0])
            quantity = st.number_input("Quantidade", min_value=1, value=1)
            if st.button("Adicionar Item"):
                if add_item_to_list(selected_list_id, product_id, quantity):
                    st.success("Item adicionado com sucesso!")
                else:
                    st.error("Erro ao adicionar item.")

            items = get_list_items(selected_list_id)
            for item in items:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"- {item['name']} (Quantidade: {item['quantity']})")
                with col2:
                    if st.button("Comprar", key=f"buy_{item['id']}"):
                        if add_to_stock(st.session_state.user['id'], item['product_id'], item['quantity']):
                            st.success(f"{item['name']} adicionado ao estoque!")
                        else:
                            st.error("Erro ao adicionar ao estoque.")

        st.header("Meu Estoque")
        stock_items = get_stock(st.session_state.user['id'])
        for item in stock_items:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"- {item['name']} (Quantidade: {item['quantity']})")
            with col2:
                quantity_to_remove = st.number_input("Quantidade a remover", min_value=1, max_value=item['quantity'], value=1, key=f"remove_qty_{item['id']}")
            with col3:
                if st.button("Dar Baixa", key=f"remove_{item['id']}"):
                    if remove_from_stock(item['id'], quantity_to_remove):
                        st.success("Baixa realizada com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao dar baixa no estoque.")

    else:
        choice = st.selectbox("Login ou Cadastro", ["Login", "Cadastro"])
        if choice == "Login":
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            if st.button("Login"):
                user = authenticate_user(username, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Usuário ou senha inválidos")
        else:
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            if st.button("Cadastrar"):
                if create_user(username, password):
                    st.success("Usuário criado com sucesso! Faça o login.")
                else:
                    st.error("Este nome de usuário já existe.")

if __name__ == "__main__":
    main()
