# Load libraries
library(tidyverse)

# Load your dataset
df <- read.csv("TUKI DEJ FILE PATH OD REZULTATA")

# Average duplicates: group by algorithm and map_size
df_avg <- df %>%
  group_by(algorithm, map_size) %>%
  summarize(avg_time = mean(time), .groups = "drop")

print(df_avg)

# ---- Function to fit model + predict ----
fit_and_predict <- function(data, algo_name) {
  
  cat("\n\n==============================\n")
  cat("Processing algorithm:", algo_name, "\n")
  cat("==============================\n")
  
  d <- data %>% filter(algorithm == algo_name)
  
  # Try exponential: time = a * exp(b * size)
  exp_model <- NULL
  try({
    exp_model <- nls(avg_time ~ a * exp(b * map_size),
                     data = d,
                     start = list(a = min(d$avg_time), b = 0.1))
  }, silent = TRUE)
  
  # Try 3rd degree polynomial
  poly_model <- lm(avg_time ~ poly(map_size, 3, raw = TRUE), data = d)
  
  # Choose best model using AIC
  if (!is.null(exp_model)) {
    aic_exp  <- AIC(exp_model)
    aic_poly <- AIC(poly_model)
    
    best <- if (aic_exp < aic_poly) {
      cat("Selected model: EXPONENTIAL\n")
      exp_model
    } else {
      cat("Selected model: POLYNOMIAL (3rd degree)\n")
      poly_model
    }
  } else {
    cat("Exponential model failed — using polynomial.\n")
    best <- poly_model
  }
  
  # Predict from sizes 4 through 20
  new_sizes <- data.frame(map_size = 4:1000)
  
  preds <- predict(best, new_sizes)
  
  results <- data.frame(
    map_size = new_sizes$map_size,
    predicted_time = preds
  )
  
  # ---- Plot actual + predicted ----
  plot <- ggplot() +
    geom_point(data = d, aes(x = map_size, y = avg_time), size = 3) +
    geom_line(data = results, aes(x = map_size, y = predicted_time), linewidth = 1) +
    labs(
      title = paste("Actual vs Predicted Solve Time for", algo_name),
      x = "Map Size (n x n)",
      y = "Solve Time (s)"
    ) +
    theme_minimal() +
    theme(plot.title = element_text(size = 16))
  
  print(plot)
  
  return(results)
}

# ---- Run for each algorithm ----
algos <- unique(df_avg$algorithm)

predictions <- list()

for (A in algos) {
  predictions[[A]] <- fit_and_predict(df_avg, A)
}

# View predictions like:
# predictions[["A*"]]
# predictions[["DFS"]]
# predictions[["BFS"]]



# ---- Combined Plot for All 3 Algorithms ----

# Build a table containing predicted curves for each algorithm
combined_predictions <- bind_rows(
  lapply(names(predictions), function(a) {
    preds <- predictions[[a]]
    preds$algorithm <- a
    preds
  })
)

# Build a table containing actual averaged data
actual_points <- df_avg %>% 
  rename(predicted_time = avg_time) %>% 
  mutate(type = "Actual")

combined_predictions$type <- "Predicted"

# Combine actual + predicted for plotting
plot_data <- bind_rows(
  actual_points %>% mutate(source = "Actual"),
  combined_predictions %>% mutate(source = "Predicted")
)

# Create combined plot
ggplot() +
  # Actual points
  geom_point(data = actual_points,
             aes(x = map_size, y = predicted_time, color = algorithm),
             size = 3, alpha = 0.8) +
  # Predicted curves
  geom_line(data = combined_predictions,
            aes(x = map_size, y = predicted_time, color = algorithm),
            linewidth = 1.2) +
  labs(title = "Solve Time Predictions (A*, DFS, BFS)",
       x = "Map Size (n x n)",
       y = "Solve Time",
       color = "Algorithm") +
  theme_minimal() +
  theme(plot.title = element_text(size = 18),
        legend.title = element_text(size = 14),
        legend.text = element_text(size = 12))


library(tidyverse)

# Filter only the sizes you want (4 to 10)
df_filtered <- df %>%
  filter(map_size >= 4, map_size <= 10)

# Compute average runtime for each (algorithm, map_size)
df_bar <- df_filtered %>%
  group_by(algorithm, map_size) %>%
  summarize(avg_time = mean(time), .groups = "drop")

# Bar plot
ggplot(df_bar, aes(x = factor(map_size), y = avg_time, fill = algorithm)) +
  geom_col(position = "dodge") +
  labs(
    title = "Average Solve Time for Each Algorithm (4×4 to 10×10)",
    x = "Map Size (n × n)",
    y = "Average Solve Time",
    fill = "Algorithm"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(size = 18),
    axis.text = element_text(size = 12),
    axis.title = element_text(size = 14),
    legend.text = element_text(size = 12),
    legend.title = element_text(size = 14)
  )

