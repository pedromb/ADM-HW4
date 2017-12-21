library(ggplot2)
data <- read.csv("data/author_subgraph_aris.csv")
g <- ggplot(data) +
    geom_line(aes(x=hop_distance, y=percentange_of_component)) +
    ggtitle("Percentage of the Component by Hop Distance") +
    ylab("Percentage of Component") +
    xlab("Maximum Hop Distance") + 
    theme(plot.title = element_text(hjust = 0.5)) +
    scale_x_discrete(limits=seq(0,10))
g