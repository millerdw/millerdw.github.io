namespace HousePriceAnalysis

module FileReader =
    open System.IO

    let ReadFileToEnd (fileName) = 
        //printfn "%A" fileName
        let lines = File.ReadAllLines(fileName)
        lines |> Array.map (fun s -> s.ToLower())
          
    let ReadCSV(path:string) = 
            ReadFileToEnd(path) |> Seq.map (fun r -> r.Replace(@"""","").Split(','))

    let ReadCSVs (directory:string) =
        Directory.GetFiles(directory)
                        |> Seq.filter (fun f -> f.EndsWith(".csv"))
                        |> Seq.collect ReadFileToEnd
                        |> Seq.map (fun r -> r.Replace(@"""","").Split(','))

module InflationReader =
    open System
    open System.Linq
    open FileReader
    
    type InflationInfo = {Date:DateTime;Level:float;Change:float;}     

    let ParseYear(year:string) = DateTime.Parse(year+"-12-31")
    let ParseYearQuarter(year:string)(quarter:string) = 
        let month = (int (quarter.Substring(1,1)))*3
        let day = match month with
                        | 3 | 12 -> 31
                        | 6 | 9 -> 30
                        | _ -> raise(new ArgumentOutOfRangeException("DateFormatter","Month of Quarter not in 3,6,9,12"))
        DateTime.Parse(year+"-"+string month+"-"+string day)
    let ParseYearMonth(year:string)(month:string) = 
        let day = match month.Substring(0,3) with
                    | "sep" | "apr" | "jun" | "nov" -> "30"
                    | "feb" when int year % 4 = 0 -> "29"
                    | "feb" when int year % 4 <> 0 -> "28"
                    | _ -> "31"
        DateTime.Parse(year+"-"+month+"-"+day)

    let DateChangeFormatter(input:string)(inputvalue:string) = 
        let sections=input.Trim().Split(' ')
        match sections.Length with
            | 1 -> ("a",ParseYear(sections.[0]),float inputvalue/100.0)
            | 2 when sections.[1].Substring(0,1)="q" -> ("q",ParseYearQuarter(sections.[0])(sections.[1]),Math.Pow(1.0+(float inputvalue/100.0),1.0/4.0)-1.0)
            | 2 when sections.[1].Substring(0,1)<>"q" -> ("m",ParseYearMonth(sections.[0])(sections.[1]),Math.Pow(1.0+(float inputvalue/100.0),1.0/12.0)-1.0)
            |_ -> raise(new ArgumentOutOfRangeException("DateChangeFormatter","too many sections in date string"))
        
    let Inflations =    
        let changes = //ReadCSV(@"C:\Users\Mille\TFS\HelloWorld\HousePriceAnalysis\HousePriceAnalysis\Data\CPI\CPI_12myoy_change.csv")
                    ReadCSV(@"D:\Documents\OneDrive\SourceControl\HelloWorld\HousePriceAnalysis\HousePriceAnalysis\Data\CPI\CPI_12myoy_change.csv")
                    //ReadCSV(@".\Data\CPI\CPI_12myoy_change.csv")
                        |> Seq.map (fun i -> DateChangeFormatter(i.[0])(i.[1]))
                        |> Seq.filter (fun (p,d,c) -> p="m")
                        |> Seq.map (fun (p,d,c) -> (d,c))
        let level = changes |> Seq.sortBy (fun (d,c) -> d) 
                            |> Seq.scan (fun (dAcc,acc) (d,c) -> (d,acc*(1.0+c))) (DateTime.Today,100.0)
        query {
            for (d1,c) in changes do
            join (d2,l) in level on (d1=d2) 
            select {Date=d1;Level=l;Change=c}
        }   |> Seq.cache

module PostcodeReader =
    let PostCodeFormat(raw:string) =
        let flat = raw.Replace(" ","").ToLower()
        match flat.Length with
            | 7 -> flat
            | 6 -> flat.Substring(0,3)+" "+flat.Substring(3,3)
            | _ -> ""
    //Postcode	
    //Positional_quality_indicator	
    //Eastings	
    //Northings	
    //Country_code	
    //NHS_regional_HA_code	
    //NHS_HA_code	
    //Admin_county_code	
    //Admin_district_code	
    //Admin_ward_code

    type PostcodeInfo={Postcode:string;Eastings:float;Northings:float}
    let Postcodes = //FileReader.ReadCSVs(@"C:\Users\Mille\TFS\HelloWorld\HousePriceAnalysis\HousePriceAnalysis\Data\Postcodes")
                    FileReader.ReadCSVs(@"D:\Documents\OneDrive\SourceControl\HelloWorld\HousePriceAnalysis\HousePriceAnalysis\Data\Postcodes")
                    //FileReader.ReadCSVs(@".\Data\Postcodes")
                        |> Seq.map (fun p -> {Postcode=PostCodeFormat(p.[0]); Eastings=float p.[2]; Northings=float p.[3]})
                        |> Seq.filter (fun p -> p.Postcode<>"" && p.Eastings*p.Northings<>0.0)
                        |> Seq.cache

    let FindPostcodeInfo(postcode:string) = 
            Postcodes |> Seq.find (fun p -> p.Postcode=postcode)

module HousePriceReader =
    open System 
    //    Transaction unique identifier
    //    Price
    //    Date of Transfer
    //    Postcode
    //    Property Type
    //    Old/New
    //    Duration
    //    PAON
    //    SAON
    //    Street
    //    Locality
    //    Town/City
    //    District
    //    County
    //    PPD Category Type
    //    Record Status - monthly file only

    type HousePriceInfo = { Postcode:string; Date:DateTime; Price:float; TownCity:string; PPD:string}
    
    let HousePrices = //FileReader.ReadCSVs(@"C:\Users\Mille\TFS\HelloWorld\HousePriceAnalysis\HousePriceAnalysis\Data\HousePrices")
                        FileReader.ReadCSVs(@"D:\Documents\OneDrive\SourceControl\HelloWorld\HousePriceAnalysis\HousePriceAnalysis\Data\HousePrices")
                        //FileReader.ReadCSVs(@".\Data\HousePrices")
                            //|> Seq.map (fun s -> new HousePriceInfo(s.[0],s.[1],s.[2],s.[3],s.[4],s.[5],s.[6],s.[7],s.[8],s.[9],s.[10],s.[11],s.[12],s.[13],s.[14],s.[15]))
                            |> Seq.map (fun h -> {  Postcode=PostcodeReader.PostCodeFormat(h.[3]); 
                                                    Date=DateTime.TryParse(h.[2]) |> (fun (b,d) -> d); 
                                                    Price=Double.TryParse(h.[1]) |> (fun (b,d) -> float d); 
                                                    TownCity=h.[11]; 
                                                    PPD=h.[14]})
                            |> Seq.filter (fun h -> h.PPD.ToLower()="a" && h.Price>10000.0 && h.Price<1000000.0)
                            |> Seq.cache

    let FindHousePriceByPostcode(postcode:string) = HousePrices |> Seq.find (fun h -> h.Postcode=PostcodeReader.PostCodeFormat(postcode))

module DataSet =
    open HousePriceReader
    open PostcodeReader
    open System

    let AllTransactions = query {  for p in Postcodes do
                                   join h in HousePrices on (p.Postcode=h.Postcode)
                                   select (p,h) }

    let SomeTransactions(filter:HousePriceInfo -> bool) = 
        let someHousePrices = HousePrices   |> Seq.filter filter
        let somePostcodes = Postcodes   
        query { for p in somePostcodes do
                join h in someHousePrices on (p.Postcode=h.Postcode)
                select (p,h) }