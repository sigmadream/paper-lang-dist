# Usage: Rscript --vanilla graph/v1/drawFigures.r summary.json output_directory
args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 2) stop("Expected summary.json and output directory")
.libPaths(c(".tools/R/library-v1", .libPaths()))
library(jsonlite)
s <- fromJSON(args[1], simplifyVector=FALSE)
out <- args[2]
dir.create(out, recursive=TRUE, showWarnings=FALSE)
routes <- names(s$rtt_route_aggregates)
labels <- sub("cpp-to-", "", routes)
colors <- c("#2878A0", "#E08B39", "#579D72")
num <- function(x) if (is.null(x)) NA_real_ else as.numeric(x)
obs <- s$observations
valid <- function(r, c=5) isTRUE(r$success[[as.character(c)]])
metric <- function(r, m) num(r$distance_metrics$delta_0[[m]]$value)
quartile_boxplot <- function(groups, col, ...) {
  b <- boxplot(groups, plot=FALSE)
  b$out <- numeric(0)
  b$group <- numeric(0)
  for(i in seq_along(groups)) {
    values <- groups[[i]]
    if(!length(values)) next
    q <- quantile(values, c(.25,.5,.75), type=7, names=FALSE)
    spread <- q[3]-q[1]
    inside <- values >= q[1]-1.5*spread & values <= q[3]+1.5*spread
    b$stats[,i] <- c(min(values[inside]),q,max(values[inside]))
    b$out <- c(b$out,values[!inside])
    b$group <- c(b$group,rep(i,sum(!inside)))
  }
  bxp(b,boxfill=col,...)
}
draw <- function(name, fun, width=9, height=5.8) {
  for (format in c("png", "pdf")) {
    path <- file.path(out, paste0(name, ".", format))
    if (format=="png") png(path, width=width, height=height, units="in", res=160)
    else pdf(path, width=width, height=height)
    par(mar=c(5,5,4,2)+.1, family="sans")
    fun()
    dev.off()
  }
}
draw("sf_distance", function() {
  y <- sapply(routes, function(r) num(s$rtt_route_aggregates[[r]]$by_confirmation[["5"]]$d_sf))
  x <- barplot(y, names.arg=labels, col=colors, ylim=c(0,1.1), ylab="d_SF (c=5)", main="Failure distance with problem-cluster 95% intervals")
  for(i in seq_along(routes)) {
    a <- s$rtt_route_aggregates[[routes[i]]]
    ci <- unlist(a$by_confirmation[["5"]]$d_sf_ci95)
    if(length(ci)==2 && ci[1]!=ci[2]) arrows(x[i],ci[1],x[i],ci[2],angle=90,code=3,length=.06)
    else if(length(ci)==2) segments(x[i]-.05,ci[1],x[i]+.05,ci[2])
    text(x[i],1.05,paste0("P=",a$problem_count,", n=",a$evaluable_count),cex=.85)
  }
})
draw("sf_confirmation", function() {
  plot(0:5, rep(0,6), type="n", ylim=c(0,1), xlab="Confirmation round trips c", ylab="p_SF(c)", main="Functional stabilization across confirmation thresholds")
  for(i in seq_along(routes)) {
    a <- s$rtt_route_aggregates[[routes[i]]]
    y <- sapply(0:5,function(c) num(a$by_confirmation[[as.character(c)]]$p_sf))
    lines(0:5,y,type="b",pch=15+i,col=colors[i],lwd=2)
  }
  nlabels <- sapply(seq_along(routes),function(i) paste0(labels[i]," (n=",s$rtt_route_aggregates[[routes[i]]]$evaluable_count,")"))
  legend("topright",nlabels,col=colors,pch=16:18,lty=1,bty="n")
})
draw("tau", function() {
  groups <- lapply(routes,function(route) sapply(Filter(function(r) r$route==route && valid(r), obs),function(r) num(r$tau)))
  names(groups) <- paste0(labels,"\nn=",lengths(groups))
  if(any(lengths(groups)>0)) quartile_boxplot(groups,col=colors,ylab="Candidate iteration tau (successful c=5)",main="Conditional stabilization time")
  else {plot.new();title("No c=5 successes: tau unavailable")}
})
draw("delta_0", function() {
  par(mfrow=c(1,3),mar=c(5,4,4,1))
  metrics <- c("token_multiset_dice","token_sequence_ratio","ast_tsed")
  titles <- c("Token multiset Dice", "Token sequence", "AST TSED")
  for(j in seq_along(metrics)) {
    groups <- lapply(routes,function(route) {
      values <- sapply(Filter(function(r) r$route==route && valid(r),obs),function(r) metric(r,metrics[j]))
      values[!is.na(values)]
    })
    names(groups) <- paste0(labels,"\nn=",lengths(groups))
    if(any(lengths(groups)>0)) quartile_boxplot(groups,col=colors,ylim=c(0,1),ylab="Delta_0",main=titles[j])
    else {plot.new();title(paste(titles[j],"unavailable"))}
    if(j==3) {
      successes <- sum(sapply(obs,valid))
      mtext(paste0("AST measured: ",sum(lengths(groups)),"/",successes),side=3,line=.2,cex=.8)
    }
  }
}, width=12)
draw("dice_tsed", function() {
  paired <- Filter(function(r) valid(r) && !is.na(metric(r,"token_multiset_dice")) && !is.na(metric(r,"ast_tsed")),obs)
  plot(0,0,type="n",xlim=c(0,1),ylim=c(0,1),xlab="Token Dice similarity",ylab="AST TSED similarity",main=paste0("Paired successful observations (n=",length(paired),")"))
  successes <- sum(sapply(obs,valid))
  mtext(paste0("Paired measurements / c=5 successes: ",length(paired),"/",successes),side=3,line=.2,cex=.8)
  for(i in seq_along(routes)) {
    g <- Filter(function(r) r$route==routes[i],paired)
    if(length(g)) points(sapply(g,function(r) 1-metric(r,"token_multiset_dice")),sapply(g,function(r) 1-metric(r,"ast_tsed")),pch=15+i,col=colors[i])
  }
  legend("bottomright",labels,col=colors,pch=16:18,bty="n")
})
writeLines(capture.output(sessionInfo()),file.path(out,"R-session.txt"))
