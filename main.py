import streamlit as st
import pandas as pd

from datetime import datetime, timedelta
from dateutil.relativedelta import *

import calendar

from sorted_months_weekdays import *

from sort_dataframeby_monthorweek import *
import plotly.graph_objects as go
import plotly.express as px


# loading DataFrame


st.set_page_config(layout="wide")

@st.cache(allow_output_mutation=True)
def cache_data():
    transactionsDf = pd.read_excel('assets/data/TransactionsDim.xlsx')
    InventoryDf=pd.read_csv ('assets/data/inventory_new.csv')
    return transactionsDf, InventoryDf

transactionsDf, InventoryDf = cache_data()


sideBarSelection = st.sidebar.selectbox(options=['EMI Simulator', 'Foot Traffic vs Digital Traffic', 'Inventory Control'], label='Select Page')

print(sideBarSelection)


# EMI Simulator
if sideBarSelection == 'EMI Simulator':

    st.header('EMI Simulator')

    col1, col2, col3 = st.columns(3)

    with col1:
        p = st.number_input('Principa   l Amount', step=100)

    with col2:
        R = st.number_input('Annual Interest in %', step=1)

    with col3:
        n = st.number_input('Number of Months', step=1)

    r = R/(12*100)

    if p and R and n is not 0:

        # Calculating interest rate per month
        r = R / (12 * 100)

        # Calculating Equated Monthly Installment (EMI)
        emi = p * r * ((1 + r) ** n) / ((1 + r) ** n - 1)
        print(emi)
        resultEmi = round(emi)
        interestPayable = round((emi * n) - p)
        totalPayment = round(emi*n)
    else:
        resultEmi = 0
        interestPayable = 0
        totalPayment = 0

    with col1:
        st.text('EMI ')
        st.subheader(str(resultEmi))

    with col2:
        st.text('Total Interest Payable')
        st.subheader(str(interestPayable))

    with col3:
        st.text('Total Payment')
        st.subheader(str(totalPayment))

    todayDate = datetime.now()

    endDate = todayDate + relativedelta(months=+n)

    dateRange = pd.date_range(todayDate.date(), endDate.date())

    emiDf = pd.DataFrame()
    emiDf['Date'] = pd.DataFrame(dateRange)

    emiDf['yearOfDate'] = emiDf['Date'].apply(lambda date: date.year)

    emiDf['monthOfDate'] = emiDf['Date'].apply(lambda date: date.month)

    monthWiseEmi = {}
    tempEmi = 0

    for i in range(1, n+1):
        tempEmi = tempEmi + emi
        monthWiseEmi[i] = round(tempEmi)

    emiDf_grouped = emiDf.groupby(by=['yearOfDate', 'monthOfDate']).count()

    emiDf_grouped.drop(emiDf_grouped.tail(1).index, inplace=True)

    emiDf_grouped['monthWiseEmi'] = monthWiseEmi.values()

    emiDf_grouped.reset_index(inplace=True)

    st.subheader('EMI Repayment Schedule')

    st.table(emiDf_grouped)


elif sideBarSelection == 'Foot Traffic vs Digital Traffic':
    st.title('Foot Traffic vs Digital Traffic')
    # To Calculate total Transaction Count


    st.write('Total Transactions Count')
    totalTransactionCount  = transactionsDf['transactionId'].count()
    st.header(totalTransactionCount)
    lineGraph = pd.DataFrame(transactionsDf.groupby('month').count()['transactionId']).reset_index()
    lineGraph = Sort_Dataframeby_Month(df=lineGraph,monthcolumnname='month')
    fig = go.Figure()
    fig = px.line(lineGraph, x="month", y="transactionId", labels = {'month': 'Month', 'transactionId': 'Transactions'})
    st.plotly_chart(fig, use_container_width = True)

    col1, col2 = st.columns(2)

    with col1:
        # To Calculate Transaction count of Store Visitors
        st.write('Transactions Count on Store')
        storeTransactionCount  = transactionsDf[transactionsDf['modeOfVisit'] == 'Store']['transactionId'].count()
        st.header(storeTransactionCount)

        lineGraph = pd.DataFrame(transactionsDf[transactionsDf['modeOfVisit']=='Store'].groupby('month').count()['transactionId']).reset_index()
        lineGraph = Sort_Dataframeby_Month(df=lineGraph,monthcolumnname='month')
        fig = go.Figure()
        fig = px.line(lineGraph, x="month", y="transactionId", labels = {'month': 'Month', 'transactionId': 'Transactions'})
        st.plotly_chart(fig, use_container_width = True)

    with col2:
        st.write('Transactions Count on Online')
        # To Calculate Transaction count of Online Visitors
        onlineTransactionCount  = transactionsDf[transactionsDf['modeOfVisit'] == 'Online']['transactionId'].count()
        st.header(onlineTransactionCount)
        lineGraph = pd.DataFrame(transactionsDf[transactionsDf['modeOfVisit']=='Online'].groupby('month').count()['transactionId']).reset_index()
        lineGraph = Sort_Dataframeby_Month(df=lineGraph,monthcolumnname='month')
        fig = go.Figure()
        fig = px.line(lineGraph, x="month", y="transactionId", labels = {'month': 'Month', 'transactionId': 'Transactions'})
        st.plotly_chart(fig, use_container_width = True)
    
    OverallAvgQuantitySold = Sort_Dataframeby_Month(pd.DataFrame(transactionsDf.groupby('month').mean()['quantity']).reset_index(), monthcolumnname = 'month')
    fig = go.Figure()
    fig = px.line(OverallAvgQuantitySold, x="month", y="quantity", labels = {'month': 'Month', 'transactionId': 'Transactions'})
    st.plotly_chart(fig, use_container_width = True)

    col1, col2 = st.columns(2)
    with col1:
        # Average Quantity mean by Store
        st.write('Average units per Customer: Store')
        st.header(round(transactionsDf[transactionsDf['modeOfVisit'] == 'Store']['quantity'].mean(), 2))
        avgQuantityOfStore = Sort_Dataframeby_Month(pd.DataFrame(transactionsDf[transactionsDf['modeOfVisit'] == 'Store'].groupby(['month']).mean()['quantity']).reset_index(), monthcolumnname = 'month')
        fig = go.Figure()
        fig = px.line(avgQuantityOfStore, x="month", y="quantity", labels = {'month': 'Month', 'quantity': 'Average Quantity'})
        st.plotly_chart(fig, use_container_width = True)

    with col2:  
        # Monthwise Average Quantity by Online DataFrame
        st.write('Average units per Customer: Online')
        st.header(round(transactionsDf[transactionsDf['modeOfVisit'] == 'Online']['quantity'].mean(), 2))
        avgQuantityOfOnline = Sort_Dataframeby_Month(pd.DataFrame(transactionsDf[transactionsDf['modeOfVisit'] == 'Online'].groupby(['month']).mean()['quantity']).reset_index(), monthcolumnname = 'month')
        fig = go.Figure()
        fig = px.line(avgQuantityOfOnline, x="month", y="quantity", labels = {'month': 'Month', 'quantity': 'Average Quantity'})
        st.plotly_chart(fig, use_container_width = True)

elif sideBarSelection == 'Inventory Control':
    st.markdown("<h2 style='text-align: center; color: black;'>Inventory Control Management</h2>", unsafe_allow_html=True)
    st.markdown("")
    st.markdown("")
    option = st.selectbox('Enter your SKU ID',InventoryDf["SKU ID"].to_list())

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
            width = 500,
            xaxis_title="Revenue",
            yaxis_title="Demand Status")
        st.plotly_chart(fig1)
    with seg2:
        st.markdown("<h3 style='text-align: center; color: black;'>Distribution of Current Stock</h3>", unsafe_allow_html=True)
        InventoryDf3 = px.data.tips()
        fig1 = px.bar(InventoryDf3, x=pr1["Current Stock Quantity"].to_list(), y=pr1["XYZ ?"].to_list(), orientation='h')
        fig1.update_layout(
            width = 500,
        xaxis_title="Current Quantity",
        yaxis_title="Demand Status")
        st.plotly_chart(fig1)

    with seg3:
        st.markdown("<h3 style='text-align: center; color: black;'>Distribution of Turn Over Ratio</h3>", unsafe_allow_html=True)
        InventoryDf3 = px.data.tips()
        fig1 = px.bar(InventoryDf3, x=pr2["trc"].to_list(), y=pr2["XYZ ?"].to_list(), orientation='h')
        fig1.update_layout(
            width = 500,
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
        autosize=True,
        margin=dict(
            l=20,
            r=20,
            b=20,
            t=20,
            pad=6))

    st.plotly_chart(fig, use_container_width = True)


# col1, col2, col3 = st.columns(3)

    st.markdown("-----------------------------------------------------")


else:
    st.write('please select any page')
