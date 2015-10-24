from Tkinter import *
import Tkconstants, tkFileDialog

class PairTrading():

    def __init__(self,rootWin):
        #Below we are setting up the graphical interface for the program

        rootWin.title("Pair Trading Analysis")
        frame = Frame(rootWin)
        frame.pack()

        self.file1_label = Label(frame,text="Stock 1:")
        self.file1_label.grid(row=0,column=0,sticky=E)
        self.file1_entry = Entry(frame,width =60)
        self.file1_entry.grid(row=0,column=1)
        self.choose_file1 = Button(frame,text="Select File",command=self.readFile1)
        self.choose_file1.grid(row=0,column=2,sticky=W)
        
        self.file2_label = Label(frame,text="Stock 2:")
        self.file2_label.grid(row=1,column=0,sticky=E)
        self.file2_entry = Entry(frame,width =60)
        self.file2_entry.grid(row=1,column=1)
        self.choose_file2 = Button(frame,text="Select File",command=self.readFile2)
        self.choose_file2.grid(row=1,column=2,sticky=W)

        self.price1_label = Label(frame,text="Current Price of Stock1:")
        self.price1_label.grid(row=2,column=0,sticky=E)

        self.price2_label = Label(frame,text="Current Price of Stock2:")
        self.price2_label.grid(row=3,column=0,sticky=E)

        self.price1_entry = Entry(frame,width = 40)
        self.price1_entry.grid(row=2,column=1)

        self.price2_entry = Entry(frame,width = 40)
        self.price2_entry.grid(row=3,column=1)

        self.num_point_label = Label(frame,text="Number of Data Points:")
        self.num_point_label.grid(row=4,column=0,sticky=E)
        self.num_point_entry = Entry(frame,width=40)
        self.num_point_entry.grid(row=4,column=1)

        self.variance_label = Label(frame,text="Variance Increment:")
        self.variance_label.grid(row=5,column=0,sticky=E)
        self.variance_entry = Entry(frame,width=40)
        self.variance_entry.grid(row=5,column=1)

        self.threshold_label = Label(frame,text="Threshold %:")
        self.threshold_label.grid(row=6,column=0,sticky=E)
        self.threshold_entry = Entry(frame,width=40)
        self.threshold_entry.grid(row=6,column=1)

        self.compute = Button(frame,text="Compute Results",command=self.match)
        self.compute.grid(row=7,columnspan=3)

        self.match_label = Label(frame,text="Valid Match?")
        self.match_label.grid(row=8,column=0,sticky=E)

        self.match_entry = Entry(frame,width = 40)
        self.match_entry.config(state="readonly")
        self.match_entry.grid(row=8,column=1)

        self.buy_label = Label(frame,text="Buy:")
        self.buy_label.grid(row=9,column=0,sticky=E)

        self.buy_entry = Entry(frame,width=40)
        self.buy_entry.config(state="readonly")
        self.buy_entry.grid(row=9,column=1)
        
        
        self.short_label = Label(frame,text="Short:")
        self.short_label.grid(row=10,column=0,sticky=E)

        self.short_entry = Entry(frame,width=40)
        self.short_entry.config(state="readonly")
        self.short_entry.grid(row=10,column=1)

        #End of GUI
        
    def readFile1(self):
        #Reading in the first file and storing the data
        self.filename = tkFileDialog.askopenfilename()
        self.file1_entry.config(state=NORMAL)
        self.file1_entry.delete(0,END)
        self.file1_entry.insert(0,self.filename)
        self.file1_entry.config(state='readonly')

        f = open(self.filename,"r")
        self.data = f.readlines()
        
    def readFile2(self):
        #Reading in the second file and storing the data
        self.filename2 = tkFileDialog.askopenfilename()
        self.file2_entry.config(state=NORMAL)
        self.file2_entry.delete(0,END)
        self.file2_entry.insert(0,self.filename2)
        self.file2_entry.config(state='readonly')

        f = open(self.filename2,"r")
        self.data2 = f.readlines()


       

        
    def match(self):
        #Getting the values for the current prices out of the entry boxes
        self.price1 = float(self.price1_entry.get())
        self.price2 = float(self.price2_entry.get())

        #Getting the number typed in for the number of data points selected
        self.datapoints = int(self.num_point_entry.get())

        #Getting the value of the variance selected
        self.variance = float(self.variance_entry.get())

        #Getting the threshold percentage selected for a good match
        self.threshold = float(self.threshold_entry.get())

        #Getting the ticker symbols for each data set by accessing the first item in each file
        self.stock1 = self.data[0]
        self.stock2 = self.data2[0]

        #Following two for loops are looping through the files to get the number of selected data points
        newdata = []
        i = 0
        for item in self.data[1:self.datapoints+1]:
            newdata.append(float(item))
            i = i+1
        

            
        newdata2 = []
        j = 0
        for item in self.data2[1:self.datapoints+1]:
            newdata2.append(float(item))
            j = j+1
        
        #If something went wrong and they could not get the same number of data points it will print an error to console
        if i != j:
            print("The amount of data points is not the same")
            
        #Storing the difference between each pair of data points
        finaldata = []
        z = 0
        while z <= i-1:
            finaldata.append(newdata2[z] - newdata[z])
            z = z+1
        
        #Calculating the average difference
        mysum = sum(finaldata)
        self.avg_diff = mysum/len(finaldata)
        print("Average Difference is:",self.avg_diff)

        #Calculating the number of points that fall within the variance
        count = 0
        for value in finaldata:
            if value >= self.avg_diff - self.variance and value <= self.avg_diff + self.variance:
                count = count + 1
                
        #Calculating the percentage that fell within variance
        print("The percentage of data points within the variance is:",count/self.datapoints)
        #If the percentage is greater than the threshold it will give a "Good Match" Result and call more analysis
        if count / self.datapoints >= self.threshold:
            self.match_entry.config(state=NORMAL)
            self.match_entry.delete(0,END)
            self.match_entry.insert(0,"Good Match")
            self.match_entry.config(state="readonly")
            self.pairAnalysis(self.price1,self.price2)
        #If the percentage is less, then it says Bad Match and its over
        else:
            self.match_entry.config(state=NORMAL)
            self.match_entry.delete(0,END)
            self.match_entry.insert(0,"Bad Match")
            self.match_entry.config(state="readonly")
            




    def pairAnalysis(self,price1,price2):#stock1,stock2)
        #Calculates the current difference in prices between the securities
        diff_price = price2 - price1
        print("Current difference in Price:",diff_price)

        
        #Calculates the adjusted prices
        if self.avg_diff >=0:
            adjusted_price1 = price1 + self.avg_diff
            
            adjusted_price2 = price2 - self.avg_diff
            
        else:
            adjusted_price1 = price1 - self.avg_diff
            
            adjusted_price2 = price2 + self.avg_diff
            
        #Determines which stock to buy and which stock to short
        if adjusted_price1 > price2:
           
            self.buy_entry.config(state=NORMAL)
            self.buy_entry.delete(0,END)
            self.buy_entry.insert(0,self.stock2)
            self.buy_entry.config(state="readonly")
            
            self.short_entry.config(state=NORMAL)
            self.short_entry.delete(0,END)
            self.short_entry.insert(0,self.stock1)
            self.short_entry.config(state="readonly")
            
            print("We need to short",self.stock1,"and buy",self.stock2)
        elif adjusted_price2 > price1:
            #print("Adjusted Price2:",adjusted_price2,"Price1:",price1)
            self.buy_entry.config(state=NORMAL)
            self.buy_entry.delete(0,END)
            self.buy_entry.insert(0,self.stock1)
            self.buy_entry.config(state="readonly")
            
            self.short_entry.config(state=NORMAL)
            self.short_entry.delete(0,END)
            self.short_entry.insert(0,self.stock2)
            self.short_entry.config(state="readonly")
            
            print("We need to short",self.stock2,"and buy",self.stock1)
            
        #If they are somehow equal it means they are in balance and there is no trade
        else:
            print("No move!")
        

    
    
rootWin = Tk()
app = PairTrading(rootWin)
rootWin.mainloop()

        
