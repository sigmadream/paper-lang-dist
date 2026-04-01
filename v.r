library(tidyverse)
library(ggplot2)

# IEEE style theme
theme_ieee <- function() {
  theme_bw(base_size = 10, base_family = "sans") +
    theme(
      plot.title = element_text(face = "bold", hjust = 0.5),
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      legend.position = "top",
      legend.justification = "center",
      legend.direction = "horizontal",
      legend.box = "horizontal",
      legend.background = element_blank(),
      legend.spacing.x = unit(0.3, "cm"),
      legend.title = element_blank(),
      axis.text = element_text(color = "black"),
      strip.background = element_rect(fill = "grey90", color = "black")
    )
}

# -----------------
# 1. Table 2: 의미 보존 여부 (Semantic Preservation)
# -----------------
df_table2 <- tibble(
  LangPair = rep(c("C++ -> C", "C++ -> Java", "C++ -> Python"), each = 4),
  Model = rep(c("qwen2.5", "qwen2.5", "gpt-5.4", "gpt-5.4"), times = 3),
  Metric = rep(c("Compile Success", "Semantic Pass"), times = 6),
  Count = c(
    2, 3, 5, 5,  # C
    3, 4, 0, 0,  # Java
    3, 3, 0, 0   # Python
  )
) %>%
  mutate(
    Percentage = Count / 5 * 100,
    LangPair = factor(LangPair, levels = c("C++ -> C", "C++ -> Java", "C++ -> Python")),
    Model_Metric = paste(Model, Metric, sep = " / ")
  )

p2 <- ggplot(df_table2, aes(x = LangPair, y = Percentage, fill = Model_Metric)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7, color = "black", linewidth = 0.5) +
  geom_text(aes(label = sprintf("%.0f%%", Percentage)), 
            position = position_dodge(width = 0.8), vjust = -0.6, size = 3.5) +
  scale_y_continuous(limits = c(0, 110), breaks = seq(0, 100, 20)) +
  scale_fill_brewer(palette = "Paired") +
  labs(
    title = "모델 및 언어 쌍에 따른 의미 보존 여부",
    x = "언어 쌍",
    y = "성공률 (%)"
  ) +
  theme_ieee() +
  guides(fill = guide_legend(nrow = 1, byrow = TRUE))

ggsave("figure_table2_success.png", p2, width = 8, height = 6, dpi = 300)
# ggsave("figure_table2_success.pdf", p2, width = 8, height = 6)
