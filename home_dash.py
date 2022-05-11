from itertools import count
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


InventoryDf=pd.read_csv (r'C:\Users\Jeevanandam\Desktop\HR Analytics\Home Appliancs Dashboard\inventory_new.csv')
st.markdown("<h2 style='text-align: center; color: black;'>Inventory Control Management</h2>", unsafe_allow_html=True)
st.markdown("")
st.markdown("")

option = st.selectbox(
    'Enter your SKU ID',
     InventoryDf["SKU ID"].to_list())


st.markdown("")
st.markdown("")

col11, col22, col33,col44 = st.columns(4)
with col11:
    pr=InventoryDf[InventoryDf["SKU ID"] == option]['Current Stock Quantity']
    for i in pr:
        st.subheader("Current Stock")
        st.subheader(round(i))

with col44:
    rp=InventoryDf[InventoryDf["SKU ID"] == option]['Stock Status']
    for i in rp:
        st.subheader("Status")
        if(i=="Out of Stock"):
            st.markdown("<h3 style='text-align: left; color: red;'>"+i+"</h3>", unsafe_allow_html=True)
        elif(i=="Below Reorder point"):
            st.markdown("<h3 style='text-align: left; color: orange;'>"+i+"</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='text-align: left; color: green;'>"+i+"</h3>", unsafe_allow_html=True)

with col33:
    pr=InventoryDf[InventoryDf["SKU ID"] == option]['Value in WH']
    for i in pr:
        st.subheader("Item Value")
        st.subheader(f"$ {i:,}")  

with col22:
    pr=InventoryDf[InventoryDf["SKU ID"] == option]['Revenue Share %']
    for i in pr:
        st.subheader("Revenue Share %")
        st.subheader(round(i,2))


col1, col2, col3 = st.columns(3)
st.markdown("")
st.markdown("")
st.markdown("-----------------------------------------------------")

for i in range(0,len(InventoryDf['Annual Revenue'])):
    InventoryDf['trc']=round((InventoryDf['Annual Revenue'])/ (InventoryDf['Value in WH']),2)

TR= round((InventoryDf['Annual Revenue'].sum())/ (InventoryDf['Value in WH'].sum()),2)

sku= InventoryDf['Current Stock Quantity'].sum()

current_value= round(InventoryDf['Value in WH'].sum(),2)
count=0
for i in InventoryDf['Do we need to order?']:
        if(i=='Yes'):
            count=count+1

col1, col2, col3,col4 = st.columns(4)

with col1:
    st.subheader("Total Items")
    st.subheader(f"{round(sku):,}")

with col2:
    st.subheader("Turn Over Ratio")
    st.subheader(f" {TR:,}")
with col3:
    st.subheader("Value of Items")
    st.subheader(f"$ {current_value:,}")  
with col4:
    st.subheader("Reorder Items")
    st.subheader(f"{count:,}")  

st.markdown("-----------------------------------------------------")
InventoryDf2=InventoryDf.drop(['SKU ID','Current Stock Quantity','Units (Nos/Kg)','Maximum Lead Time (days)','Unit Price','today',
'Annual Sale Quantity','Revenue Share %','Cummulative share','Average Weekly Demand','CV','CV rank','Value in WH','ABC rank',
'Peak Weekly Demand','Safety Stock','Re order point','Do we need to order?','Stock Status','Average Lead Time (days)','SD of Weekly Demand','trc'],axis=1)

InventoryDf4=InventoryDf.drop(['SKU ID','Annual Revenue','Units (Nos/Kg)','Maximum Lead Time (days)','Unit Price','today',
'Annual Sale Quantity','Revenue Share %','Cummulative share','Average Weekly Demand','CV','CV rank','Value in WH','ABC rank',
'Peak Weekly Demand','Safety Stock','Re order point','Do we need to order?','Stock Status','Average Lead Time (days)','SD of Weekly Demand','trc'],axis=1)

InventoryDf5=InventoryDf.drop(['SKU ID','Annual Revenue','Units (Nos/Kg)','Maximum Lead Time (days)','Unit Price','today',
'Annual Sale Quantity','Revenue Share %','Cummulative share','Average Weekly Demand','CV','CV rank','Value in WH','ABC rank',
'Peak Weekly Demand','Safety Stock','Re order point','Do we need to order?','Stock Status','Average Lead Time (days)','SD of Weekly Demand','Current Stock Quantity'],axis=1)
# InventoryDf3['ASX code'] = InventoryDf2[['ASX code']].copy()
InventoryDf2=InventoryDf2.groupby(['ABC ?','XYZ ?'],as_index=False)['Annual Revenue'].sum()
#InventoryDf2.groupby(['ABC ?','XYZ ?']).size().reset_index().groupby('XYZ ?')[[0]].sum()
InventoryDf4=InventoryDf4.groupby(['ABC ?','XYZ ?'],as_index=False)['Current Stock Quantity'].sum()
InventoryDf5=InventoryDf5.groupby(['ABC ?','XYZ ?'],as_index=False)['trc'].sum()


option1 = st.selectbox('',list(set(InventoryDf2["ABC ?"].to_list())))
st.markdown("")
st.markdown("")
pr=InventoryDf2[InventoryDf2["ABC ?"] == option1]
pr=pr.drop(['ABC ?'],axis=1)
pr.index.names = [None]

pr1=InventoryDf4[InventoryDf4["ABC ?"] == option1]
pr1=pr1.drop(['ABC ?'],axis=1)
pr1.index.names = [None]

pr2=InventoryDf5[InventoryDf5["ABC ?"] == option1]
pr2=pr2.drop(['ABC ?'],axis=1)
pr2.index.names = [None]

seg1, seg2, seg3 = st.columns(3)

with seg1:
    st.markdown("<h3 style='text-align: center; color: black;'>Distribution of Annual Revenue</h3>", unsafe_allow_html=True)
    InventoryDf3 = px.data.tips()
    fig1 = px.bar(InventoryDf3, x=pr["Annual Revenue"].to_list(), y=pr["XYZ ?"].to_list(), orientation='h')
    fig1.update_layout(
        xaxis_title="Revenue",
        yaxis_title="Demand Status")
    st.plotly_chart(fig1)
with seg2:
    st.markdown("<h3 style='text-align: center; color: black;'>Distribution of Current Stock</h3>", unsafe_allow_html=True)
    InventoryDf3 = px.data.tips()
    fig1 = px.bar(InventoryDf3, x=pr1["Current Stock Quantity"].to_list(), y=pr1["XYZ ?"].to_list(), orientation='h')
    fig1.update_layout(
        xaxis_title="Current Quantity",
        yaxis_title="Demand Status")
    st.plotly_chart(fig1)

with seg3:
    st.markdown("<h3 style='text-align: center; color: black;'>Distribution of Turn Over Ratio</h3>", unsafe_allow_html=True)
    InventoryDf3 = px.data.tips()
    fig1 = px.bar(InventoryDf3, x=pr2["trc"].to_list(), y=pr2["XYZ ?"].to_list(), orientation='h')
    fig1.update_layout(
        xaxis_title="Turn over Ratio",
        yaxis_title="Demand Status")
    st.plotly_chart(fig1)



st.markdown("-----------------------------------------------------")

st.markdown("")
st.markdown("")


st.markdown("<h3 style='text-align: center; color: black;'>Distribution Of ABC</h3>", unsafe_allow_html=True)



InventoryDf1 = px.data.medals_long()

fig = px.area(InventoryDf, x=InventoryDf['ABC rank'].to_list(), y=InventoryDf["Cummulative share"].to_list(), color=InventoryDf["ABC ?"].to_list() )

fig.update_layout(
        xaxis_title="Quantity Of Items In WH",
        yaxis_title="Revenue Share",
        autosize=False,
        width=1900,
        height=500,
        margin=dict(
            l=20,
            r=20,
            b=20,
            t=20,
            pad=6))

st.plotly_chart(fig)


# col1, col2, col3 = st.columns(3)

st.markdown("-----------------------------------------------------")


# TR= round((InventoryDf['Annual Revenue'].sum())/ (InventoryDf['Value in WH'].sum()),2)

# sku= InventoryDf['SKU ID'].count()

# current_value= round(InventoryDf['Value in WH'].sum(),2)

# col1, col2, col3 = st.columns(3)

# with col1:
#     st.subheader("Items In Wharehouse")
#     st.subheader(f"{round(sku,2):,}")

# with col2:
#     st.subheader("Turn Over Ratio")
#     st.subheader(f" {TR:,}")
# with col3:
#     st.subheader("Current Value of Items In Wharehouse")
#     st.subheader(f"$ {current_value:,}")  

# st.markdown("-----------------------------------------------------")


# InventoryDf2=InventoryDf.drop(['SKU ID','Current Stock Quantity','Units (Nos/Kg)','Maximum Lead Time (days)','Unit Price','today',
# 'Annual Sale Quantity','Revenue Share %','Cummulative share','Average Weekly Demand','CV','CV rank','Value in WH','ABC rank',
# 'Peak Weekly Demand','Safety Stock','Re order point','Do we need to order?','Stock Status','Average Lead Time (days)','SD of Weekly Demand'],axis=1)

# # InventoryDf3['ASX code'] = InventoryDf2[['ASX code']].copy()
# InventoryDf2=InventoryDf2.groupby(['ABC ?','XYZ ?'],as_index=False)['Annual Revenue'].sum()
# #InventoryDf2.groupby(['ABC ?','XYZ ?']).size().reset_index().groupby('XYZ ?')[[0]].sum()

# option1 = st.selectbox('',list(set(InventoryDf2["ABC ?"].to_list())))

# pr=InventoryDf2[InventoryDf2["ABC ?"] == option1]
# pr=pr.drop(['ABC ?'],axis=1)
# pr.index.names = [None]

# seg1, seg2, seg3 = st.columns(3)

# with seg1:
#     InventoryDf = px.data.tips()
#     fig1 = px.bar(InventoryDf, x=pr[""], y="day", orientation='h')
#     fig1.update_layout(
#             autosize=False,
#             width=800,
#             height=1000,
#             margin=dict(
#                 l=20,
#                 r=20,
#                 b=20,
#                 t=20,
#                 pad=10))
#     st.plotly_chart(fig1)

