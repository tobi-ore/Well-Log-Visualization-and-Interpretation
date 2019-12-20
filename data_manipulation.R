library(ggplot2)
library(gtable)
library(grid)
library(gridExtra)
library(tidyverse)

#Create Subdirectory called output where all output folders will be stored
dir.create(file.path(".", "Output"))

#Create a new directory to save the images created
dir.create(file.path("./Output", "Log_Images"))

#Create a new directory to save the new dataframe created for each well
dir.create(file.path("./Output", "Interpreted_Logs"))

#Create a new directory to save the new VSh images created for each well
dir.create(file.path("./Output", "VSH_Images"))


#data visualization
for(file in list.files(path = "./data_csv")){
  data <- read.csv(sprintf("./data_csv/%s", file), header=T)
  
  well <- sub(pattern = "(.*)\\..*$", replacement = "\\1", basename(file))  #removes the extension in the filename
  
  #Gamma Ray Plot  
  p1 <- ggplot(data,aes(DEPT,GR)) + geom_line(size=0.3)+
    coord_flip() +
    scale_x_reverse() +
    theme(plot.margin = unit(c(0,0.1,0,0), "cm"),
          plot.background = element_blank()) +
    ggtitle("GR")
  
  #Resistivity Plot
  p2 <- ggplot(data,aes(DEPT,LL8)) + geom_line(size=0.3, color='blue') + scale_y_log10() + 
    coord_flip() + scale_x_reverse() +
    theme(axis.text.y = element_blank(), 
          axis.ticks.y = element_blank(), 
          axis.title.y = element_blank(),
          plot.margin = unit(c(0,0.1,0,0), "cm"),
          plot.background = element_blank()) +
    ggtitle("Resistivity")
  
  #Density Plot
  p3 <- ggplot(data,aes(DEPT,RHOB)) + geom_line(size=0.3, color='green') + 
    coord_flip() + scale_x_reverse() +
    theme(axis.text.y = element_blank(), 
          axis.ticks.y = element_blank(), 
          axis.title.y = element_blank(),
          plot.margin = unit(c(0,0.1,0,0), "cm"),
          plot.background = element_blank()) +
    ggtitle("Density")
  
  #Neutron Plot
  p4 <- ggplot(data,aes(DEPT,NPHI)) + geom_line(size=0.3, color='brown') + 
    coord_flip() + scale_x_reverse() +
    theme(axis.text.y = element_blank(), 
          axis.ticks.y = element_blank(), 
          axis.title.y = element_blank(),
          plot.margin = unit(c(0,0.1,0,0), "cm"),
          plot.background = element_blank()) +
    ggtitle("Neutron")
  
  #Sonic Plot
  p5 <- ggplot(data,aes(DEPT,DT)) + geom_line(size=0.3, color='red') + 
    coord_flip() + scale_x_reverse() + scale_y_reverse() +
    theme(axis.text.y = element_blank(), 
          axis.ticks.y = element_blank(), 
          axis.title.y = element_blank(),
          plot.margin = unit(c(0,0.1,0,0), "cm"),
          plot.background = element_blank()) +
    ggtitle("Sonic")
  
  #convert the ggplot output into a gtable
  gt1 <- ggplotGrob(p1)
  gt2 <- ggplotGrob(p2)
  gt3 <- ggplotGrob(p3)
  gt4 <- ggplotGrob(p4)
  gt5 <- ggplotGrob(p5)
  
  newWidth = unit.pmax(gt1$widths[2:3], gt2$widths[2:3])
  
  gt1$widths[2:3] = as.list(newWidth)
  gt2$widths[2:3] = as.list(newWidth)
  gt3$widths[2:3] = as.list(newWidth)
  gt4$widths[2:3] = as.list(newWidth)
  gt5$widths[2:3] = as.list(newWidth)
  
  
  gt = gtable(widths = unit(c(1, 1, 1, 1, 1, .3), "null"), height = unit(20, "null"))
  
  # Insert gt1, gt2, gt3, gt4 and gt5 into the new gtable
  gt <- gtable_add_grob(gt, gt1, 1, 1)
  gt <- gtable_add_grob(gt, gt2, 1, 2)
  gt <- gtable_add_grob(gt, gt3, 1, 3)
  gt <- gtable_add_grob(gt, gt4, 1, 4)
  gt <- gtable_add_grob(gt, gt5, 1, 5)
  
  grid.newpage()
  grid.draw(gt)
  ggsave(sprintf("./Output/Log_Images/%s.png", well), plot=gt)
}

#Petrophysical calculation
for(file in list.files(path = "./data_csv")){
  well <- sub(pattern = "(.*)\\..*$", replacement = "\\1", basename(file))
  sub_data <- read.csv(sprintf("./data_csv/%s", file), header=T)
  
  #Volume of SHale Calculation
  sub_data <- sub_data %>%
    mutate(VSH_linear = (GR - min(GR, na.rm=TRUE))/(max(GR, na.rm=TRUE) - min(GR, na.rm=TRUE)),
           VSH_larionov_young = 0.083*(2**(3.7*VSH_linear)-1),
           VSH_larionov_old = 0.33*(2**(2*VSH_linear)-1),
           VSH_clavier = 1.7-(3.38-(VSH_linear + 0.7)**2)**0.5,
           VSH_steiber = 0.5*VSH_linear/(1.5 - VSH_linear))
 
   #Porosity estimation
  den_ma <- 2.65
  den_fl <- 1.1
  sub_data <- sub_data %>%
    mutate(PHID = (RHOB - den_ma)/(den_fl-den_ma),
           PHIND = ((NPHI**2 + PHID**2)/2)**0.5)
 
  write.csv(sub_data,file=sprintf("./Output/Interpreted_Logs/%s.csv", well))
  
  #store the new interpreted well log data in the global environment as the well name
  assign(as.character(well), sub_data, envir= .GlobalEnv)
}

#Plotting the Estimated Vshale
for(file in list.files(path = "./Output/Interpreted_Logs")){
  data <- read.csv(sprintf("./Output/Interpreted_Logs/%s", file), header=T)
  well <- sub(pattern = "(.*)\\..*$", replacement = "\\1", basename(file))
  
  #Gamma Ray Plot
  p1 <- ggplot(data=data,mapping=aes(x = DEPT,y = GR)) + geom_line(size=0.3)+
    coord_flip() +
    scale_x_reverse() +
    theme(plot.margin = unit(c(0,0.2,0,0), "cm"),
          plot.background = element_blank())
  
  colors <- c("VSH_linear" = "blue", "VSH_larionov_young" = "red", "VSH_larionov_old" = "orange",
              "VSH_clavier"="green", "VSH_steiber"='purple')
  
  #The Volume of SHale plot
  p2 <- ggplot(data, aes(x = DEPT)) + 
    geom_line(aes(y = VSH_linear, color='VSH_linear'), size=0.1) + 
    geom_line(aes(y = VSH_larionov_young, color='VSH_larionov_young'), size=0.1) +
    geom_line(aes(y = VSH_larionov_old, color='VSH_larionov_old'), size=0.1) +
    geom_line(aes(y = VSH_clavier, color='VSH_clavier'), size=0.1) +
    geom_line(aes(y = VSH_steiber, color='VSH_steiber'), size=0.1) +
    labs(y = "Vshale",
         color = "Legend") +
    scale_color_manual(values = colors) +
    coord_flip() + scale_x_reverse() +
    theme(axis.text.y = element_blank(), 
          axis.ticks.y = element_blank(), 
          axis.title.y = element_blank(),
          plot.margin = unit(c(0,0.5,0,0), "cm"),
          plot.background = element_blank())
  
  gt1 <- ggplotGrob(p1)
  gt2 <- ggplotGrob(p2)
  
  
  newWidth = unit.pmax(gt1$widths[2:3], gt2$widths[2:3])
  
  gt1$widths[2:3] = as.list(newWidth)
  gt2$widths[2:3] = as.list(newWidth)
  
  gt = gtable(widths = unit(c(1, 1.7, .2), "null"), height = unit(50, "null"))
  
  # Insert gt1 and gt2 into the new gtable
  gt <- gtable_add_grob(gt, gt1, 1, 1)
  gt <- gtable_add_grob(gt, gt2, 1, 2)
  
  grid.newpage()
  grid.draw(gt)
  ggsave(sprintf("./Output/VSH_Images/%s.png", well), plot=gt)
}