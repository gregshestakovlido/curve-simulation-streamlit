import streamlit as st
import pandas as pd
import CurveSim


if 'st_eth_pool' not in st.session_state:
    st_eth_pool = CurveSim.create_steth_pool()
    st.session_state['st_eth_pool'] = st_eth_pool


st.title('Curve pool simulation')



st.sidebar.write('**Pool operations**')
refresh= st.sidebar.button('Return pool to initial state')
if refresh:
    st_eth_pool= CurveSim.create_steth_pool()
    st.session_state['st_eth_pool'] = st_eth_pool


st.sidebar.write('Pool operations')
with st.sidebar.form("Exchange"):
    st.write('Exchange')

    exchange_type=st.selectbox(
        'Choose exchange type',
         ('ETH->stETH', 'stETH->ETH'))
    amount=st.number_input('Enter amount',step=1)
    exchange=st.form_submit_button('Exchange')
    if exchange:
        if exchange_type=='ETH->stETH':
            st.session_state['st_eth_pool'].exchange_tokens('eth','steth',amount)

        else:
            st.session_state['st_eth_pool'].exchange_tokens('steth','eth',amount)

with st.sidebar.form("Add liquidity"):
    st.write('Add liquidity')


    eth_amount=st.number_input('Enter ETH amount',step=1)
    steth_amount=st.number_input('Enter stETH amount',step=1)
    amounts=[]
    amounts.append(eth_amount*(10**18))
    amounts.append(steth_amount*(10**18))
    add_liquidity=st.form_submit_button('Add liquidity')
    if add_liquidity:
        st.session_state['st_eth_pool'].add_liquidity(amounts)

with st.sidebar.form("Withdraw liquidity"):
    st.write('Withraw one token')
    exchange_type = st.selectbox(
        'Choose token',
        ('ETH', 'stETH'))

    withradw_amount=st.number_input('Enter ETH amount',step=1)

    withdraw_liquidity=st.form_submit_button('Withdraw liquidity')
    if withdraw_liquidity:
        if exchange_type=='ETH':
            st.session_state['st_eth_pool'].remove_liquidity_one_coin(withradw_amount*10**18,0)
        if exchange_type == 'stETH':
            st.session_state['st_eth_pool'].remove_liquidity_one_coin(withradw_amount * 10 ** 18,1)


col1, col2, col3= st.columns(3)

with col1:

    st.subheader(f"ETH balance: {st.session_state['st_eth_pool'].x[0]/10**18:.2f}")
    st.subheader(f"ETH -> stETH exchange rate is {st.session_state['st_eth_pool'].info()['ETH_stETH']}")
with col2:
    st.header("")
with col3:
    st.subheader(f"stETH balance: {st.session_state['st_eth_pool'].x[1]/10**18:.2f}")
    st.subheader(f"stETH -> ETH exchange rate is {st.session_state['st_eth_pool'].info()['stETH_ETH']}")

