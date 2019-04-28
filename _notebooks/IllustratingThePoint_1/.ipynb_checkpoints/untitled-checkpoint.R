
library('WDI')
library('reshape2')
library('ggplot2')
library('dplyr')
library('magrittr')


dataItems <-
    rbind(c('SI.POV.GINI','GiniCoefficient'),
          c('SI.DST.FRST.20','IncomeShare1stQuintile'),
          c('SI.DST.02ND.20','IncomeShare2ndQuintile'),
          c('SI.DST.03RD.20','IncomeShare3rdQuintile'),
          c('SI.DST.04TH.20','IncomeShare4thQuintile'),
          c('SI.DST.05TH.20','IncomeShare5thQuintile'),
          c('BN.CAB.XOKA.GD.ZS','CurrentAccountBalancePctGDP'),
          c('NE.TRD.GNFS.ZS','TradePctGDP'),
          c('NE.IMP.GNFS.ZS','ImportsPctGDP'),
          c('NE.EXP.GNFS.ZS','ExportsPctGDP'),
          c('TM.VAL.MANF.ZS.UN','ManufacturesPctMerchImports'),
          c('TX.VAL.MANF.ZS.UN','ManufacturesPctMerchExports'),
          c('TX.VAL.TECH.MF.ZS','TechPctManufacturesExports'),
          c('TM.VAL.MRCH.OR.ZS','PctMerchImportsFromLowMiddle'),
          c('TX.VAL.MRCH.HI.ZS','PctMerchExportsToHigh'),
          c('BM.GSR.MRCH.CD','GoodsImportsUSD'),
          c('BM.GSR.NFSV.CD','ServiceImportsUSD'),
          c('BN.GSR.MRCH.CD','NetGoodsTradesUSD'),
          c('BN.GSR.GNFS.CD','NetTradesUSD')  )

key <- c('iso','country','year')


downloadWDIData <- function() {
    dat = WDI(indicator=dataItems[,1], 
              #country=c('MX','TH','CN','TW','DE','FR','US','GB'), 
              start=1960, end=2018)
    colnames(dat) <- c(key,dataItems[,2])
    
    #calculations
    dat$CurrentAccountDeficitFlag <- ifelse(dat$CurrentAccountBalancePctGDP<0,'Deficit','Surplus')
    dat$TotalAbsoluteTradesPctGDP <- dat$ExportsPctGDP+dat$ImportsPctGDP
    dat$NetTradesPctGDP <- dat$ExportsPctGDP-dat$ImportsPctGDP
    dat$GoodsExportsUSD <- dat$NetGoodsTradesUSD+dat$GoodsImportsUSD
    dat$NetServiceTradesUSD <- dat$NetTradesUSD-dat$NetGoodsTradesUSD
    dat$ServiceExportsUSD <- dat$NetServiceTradesUSD+dat$ServiceImportsUSD
    dat$ImportsUSD <- dat$GoodsImportsUSD+dat$ServiceImportsUSD

    dat$GDPUSD <- dat$ImportsUSD/dat$ImportsPctGDP
    dat$GoodsImportsPctGDP <- dat$GoodsImportsUSD/dat$GDPUSD
    dat$GoodsExportsPctGDP <- dat$GoodsExportsUSD/dat$GDPUSD
    dat$ServiceImportsPctGDP <- dat$ServiceImportsUSD/dat$GDPUSD
    dat$ServiceExportsPctGDP <- dat$ServiceExportsUSD/dat$GDPUSD
    dat$NetGoodsTradesPctGDP <- dat$NetGoodsTradesUSD/dat$GDPUSD
    dat$NetServiceTradesPctGDP <- dat$NetServiceTradesUSD/dat$GDPUSD
    
    dat
}

#moltenData <- 
#    melt(data=dat,
#         id.vars=key,
#         variable.name='DataItem',
#         value.name='DataValue')


bricsCountries<-c('Brazil','Russian Federation','India','China','South Africa')
civetsCountries<-c('Colombia','Indonesia','Vietnam','Egypt','Turkey')
next11Countries<-c('Bangladesh','Egypt', 'Indonesia', 'Iran', 'Korea', 'Mexico', 'Nigeria', 'Pakistan', 'Philippines', 'Turkey', 'Vietnam')
countries<-c('France','Germany','United States','United Kingdom','Canada')
otherCountries<-c('Mexico','Thailand')


ggPlotAxes <- function(data,xAxis,yAxis) {
    data[!is.na(data[,xAxis]) 
           & !is.na(data[,yAxis]),
         c(key,xAxis,yAxis)] %>% {
            colnames(.) <- c(key,'xAxis','yAxis')
            .
        } %>%
        ggplot(aes(x=xAxis, y=yAxis, color=country, group=country)) +
            labs(x=xAxis,y=yAxis)
}

