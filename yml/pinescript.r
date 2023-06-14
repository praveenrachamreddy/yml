//@version=5
indicator(title="Moving Average + Supertrend + Parabolic SAR", shorttitle="MA+ST+PSAR", overlay=true)

len = input.int(20, minval=1, title="Moving Average Length")
src = input(close, title="Source")
offset = input.int(title="Offset", defval=0, minval=-500, maxval=500)

maValue = ta.sma(src, len)
plot(maValue, color=color.blue, title="Moving Average", offset=offset)

atrPeriod = input(9, "ATR Length")
factor = input.float(1.5, "Supertrend Factor", step=0.01)

[supertrendUp, directionUp] = ta.supertrend(factor, atrPeriod)
[supertrendDown, directionDown] = ta.supertrend(factor, atrPeriod)

plot(directionUp < 0 ? supertrendUp : na, "Up Trend", color=color.green, style=plot.style_linebr, offset=offset)
plot(directionDown < 0 ? na : supertrendDown, "Down Trend", color=color.red, style=plot.style_linebr, offset=offset)

psarStart = input(0.02, "PSAR Start")
psarIncrement = input(0.02, "PSAR Increment")
psarMaximum = input(0.2, "PSAR Max Value")

psarValue = ta.sar(psarStart, psarIncrement, psarMaximum)
plot(psarValue, "Parabolic SAR", style=plot.style_cross, color=color.red, offset=offset)
