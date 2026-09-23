library(ggplot2)

# IEEE / Engineering style theme
theme_engineering <- function() {
  theme_bw(base_size = 12, base_family = "AppleGothic") +
    theme(
      plot.title = element_text(face = "bold", hjust = 0.5, size = 14),
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      panel.border = element_rect(color = "black", linewidth = 1),
      legend.position = "top",
      legend.justification = "center",
      legend.direction = "horizontal",
      legend.box = "horizontal",
      legend.background = element_blank(),
      legend.spacing.x = unit(0.3, "cm"),
      legend.title = element_blank(),
      axis.text = element_text(color = "black", size = 11),
      axis.title = element_text(size = 12, face = "bold"),
      strip.background = element_rect(fill = "grey90", color = "black")
    )
}

# -----------------
# 1. Table 1: 변경 횟수 거리와 의미 보존 (Iterations & Pass Rate)
# -----------------
df_iter <- data.frame(
  LangPair = rep(c("C++ → C", "C++ → Java", "C++ → Python"), each = 2),
  Model = rep(c("qwen2.5", "gpt-5.4"), times = 3),
  AvgIter = c(2.2, 5.4, 2.4, 1.2, 2.2, 1.0),
  PassRate = c(100, 100, 100, 0, 100, 0)
)
df_iter$LangPair <- factor(df_iter$LangPair, levels = c("C++ → C", "C++ → Java", "C++ → Python"))
df_iter$Model <- factor(df_iter$Model, levels = c("qwen2.5", "gpt-5.4"))

p_iter <- ggplot(df_iter, aes(x = LangPair, y = AvgIter, fill = Model)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7, color = "black", linewidth = 0.6) +
  geom_text(aes(label = sprintf("반복 횟수: %.1f\n(보존율: %d%%)", AvgIter, PassRate)), 
            position = position_dodge(width = 0.8), vjust = -0.2, size = 3.0, lineheight = 1.1) +
  scale_y_continuous(limits = c(0, max(df_iter$AvgIter) * 1.3), expand = expansion(mult = c(0, 0.05))) +
  scale_fill_manual(values = c("qwen2.5" = "#4A5568", "gpt-5.4" = "#CBD5E0")) +
  labs(
    title = "평균 반복 횟수 및 의미 보존 통과율",
    x = "언어 쌍",
    y = "평균 반복 횟수 (회)"
  ) +
  theme_engineering()

ggsave("figure_iterations.png", p_iter, width = 7, height = 5, dpi = 300)
ggsave("figure_iterations.pdf", p_iter, width = 7, height = 5, device = cairo_pdf)

# -----------------
# 2. Table 2: MOSS 유사도 (MOSS Similarity)
# -----------------
df_moss <- data.frame(
  LangPair = rep(c("C++ → C", "C++ → Java", "C++ → Python"), each = 2),
  Model = rep(c("qwen2.5", "gpt-5.4"), times = 3),
  Mean = c(19.3, 25.4, 63.8, 36.7, 0.0, 36.4),
  SD = c(22.5, 24.4, 14.2, 41.0, 0.0, 23.8)
)
df_moss$LangPair <- factor(df_moss$LangPair, levels = c("C++ → C", "C++ → Java", "C++ → Python"))
df_moss$Model <- factor(df_moss$Model, levels = c("qwen2.5", "gpt-5.4"))

p_moss <- ggplot(df_moss, aes(x = LangPair, y = Mean, fill = Model)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7, color = "black", linewidth = 0.6) +
  geom_errorbar(aes(ymin = pmax(0, Mean - SD), ymax = Mean + SD), 
                position = position_dodge(width = 0.8), width = 0.25, linewidth = 0.6) +
  geom_text(aes(y = Mean + SD + 3, label = sprintf("%.1f", Mean)), 
            position = position_dodge(width = 0.8), size = 3.5) +
  scale_y_continuous(limits = c(0, max(df_moss$Mean + df_moss$SD) * 1.15), breaks = seq(0, 100, 20), expand = expansion(mult = c(0, 0.05))) +
  scale_fill_manual(values = c("qwen2.5" = "#4A5568", "gpt-5.4" = "#CBD5E0")) +
  labs(
    title = "번역 결과의 MOSS 유사도",
    x = "언어 쌍",
    y = "MOSS 유사도 (%)"
  ) +
  theme_engineering()

ggsave("figure_moss.png", p_moss, width = 7, height = 5, dpi = 300)
ggsave("figure_moss.pdf", p_moss, width = 7, height = 5, device = cairo_pdf)

