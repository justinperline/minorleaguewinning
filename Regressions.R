model <- lm(SixYearWAR ~ ProspectProxyFinal, data=GroupedByPlayer)
summary(model)

model <- lm(SixYearWAR ~ POPct + CHPct, data=GroupedByPlayer)
summary(model)

GroupedByPlayer$TotalGames <- GroupedByPlayer$TotalWins + GroupedByPlayer$TotalLosses
model <- lm(SixYearWAR ~ TotalWins + TotalGames, data=GroupedByPlayer)
summary(model)

model <- lm(SixYearWAR ~ Frk + FrkPct + Rk + RkPct + Short + ShortPct + A + APct + High + HighPct + AA + AAPct + AAA + AAAPct, data=GroupedByPlayer)
summary(model)

model <- lm(SixYearWAR ~ Frk + FrkPct + Rk + RkPct + Short + ShortPct + A + APct + High + HighPct + AA + AAPct + AAA + AAAPct + POPct + CHPct + Prospect_WPS, data=GroupedByPlayer)
summary(model)

model <- lm(Majors ~ Frk + FrkPct + Rk + RkPct + Short + ShortPct + A + APct + High + HighPct + AA + AAPct + AAA + AAAPct + POPct + CHPct + Prospect_Majors, data=GroupedByPlayer)
summary(model)
