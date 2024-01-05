import tensorflow as tf
import numpy as np
import pandas as pd
import MetaTrader5 as mt

def calculate_rsi(prices, period=14):
    deltas = np.diff(prices)
    seed = deltas[:period + 1]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:period] = 100.0 - 100.0 / (1.0 + rs)

    for i in range(period, len(prices)):
        delta = deltas[i - 1]
        if delta > 0:
            upval = delta
            downval = 0.0
        else:
            upval = 0.0
            downval = -delta

        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period
        rs = up / down
        rsi[i] = 100.0 - 100.0 / (1.0 + rs)

    return rsi
def calculate_macd(prices, short_period=12, long_period=26, signal_period=9):
    ema_short = calculate_ema(prices, short_period)
    ema_long = calculate_ema(prices, long_period)
    macd_line = ema_short - ema_long
    signal_line = calculate_ema(macd_line, signal_period)
    histogram = macd_line - signal_line

    return macd_line, signal_line, histogram
def calculate_ema(prices, period=20):
    ema = np.zeros_like(prices)
    ema[0] = prices[0]

    alpha = 2 / (period + 1)
    for i in range(1, len(prices)):
        ema[i] = (1 - alpha) * ema[i-1] + alpha * prices[i]

    return ema


def calculate_tma(prices, period=20):
    weights = np.arange(1, period + 1)
    tma = np.convolve(prices, weights, 'valid') / weights.sum()

    return tma
def calculate_bollinger_bands(prices, period=20, std_dev=2):
    sma = calculate_sma(prices, period)
    std = np.std(prices[-period:])
    upper_band = sma + std_dev * std
    lower_band = sma - std_dev * std

    return upper_band, lower_band
import math
import numpy as np
import ta

pattern_list = [
    "OnNeckBearish",
    "RisingWindowBullish",
    "FallingWindowBearish",
    "FallingThreeMethodsBullish",
    "FallingThreeMethodsBearish",
    "TweezerBottomBullish",
    "TweezerTopBearish",
    "DarkCloudCoverBearish",
    "UpsideTasukiGapBullish",
    "DownsideTasukiGapBearish",
    "EveningDojiStarBearish",
    "Doji",
    "DojiStarBullish",
    "DojiStarBearish",
    "MorningDojiStarBullish",
    "PiercingBullish",
    "HammerBullish",
    "HangingManBearish",
    "ShootingStarBearish",
    "InvertedHammerBullish",
    "MorningStarBullish",
    "EveningStarBearish",
    "MarubozuWhiteBullish",
    "MarubozuBlackBearish",
    "GravestoneDojiBearish",
    "DragonflyDojiBullish",
    "HaramiCrossBullish",
    "HaramiCrossBearish",
    "HaramiBullish",
    "HaramiBearish",
    "LongLowerShadowBullish",
    "LongUpperShadowBearish",
    "SpinningTopWhite",
    "SpinningTopBlack",
    "ThreeWhiteSoldiersBullish",
    "ThreeBlackCrowsBearish",
    "EngulfingBullish",
    "EngulfingBearish",
    "AbandonedBabyBullish",
    "AbandonedBabyBearish",
    "TriStarBullish",
    "TriStarBearish",
    "KickingBullish",
    "KickingBearish",
]

def Pattern(data, i):
    candles = data[i:i+9].T
    o0, h0, l0, c0 = candles[0]
    o1, h1, l1, c1 = candles[1]
    o2, h2, l2, c2 = candles[2]
    o3, h3, l3, c3 = candles[3]
    o4, h4, l4, c4 = candles[4]
    o5, h5, l5, c5 = candles[5]
    o6, h6, l6, c6 = candles[6]
    o7, h7, l7, c7 = candles[7]
    o8, h8, l8, c8 = candles[8]

    C_BodyHi = np.maximum(c0, o0)
    C_BodyLo = np.minimum(c0, o0)
    C_BodyHi1 = np.maximum(c1, o1)
    C_BodyLo1 = np.minimum(c1, o1)
    C_BodyHi2 = np.maximum(c2, o2)
    C_BodyLo2 = np.minimum(c2, o2)
    C_BodyHi3 = np.maximum(c3, o3)
    C_BodyLo3 = np.minimum(c3, o3)
    C_BodyHi4 = np.maximum(c4, o4)
    C_BodyLo4 = np.minimum(c4, o4)

    C_Body = C_BodyHi - C_BodyLo
    C_Body1 = C_BodyHi1 - C_BodyLo
    C_Body2 = C_BodyHi2 - C_BodyLo2
    C_Body3 = C_BodyHi3 - C_BodyLo3
    C_Body4 = C_BodyHi4 - C_BodyLo4

    BodyLength = c0 - o0
    BodyLength1 = c1 - o1
    BodyLength2 = c2 - o2
    BodyLength3 = c3 - o3
    BodyLength4 = c4 - o4

    ShadowHi = h0 - np.maximum(c0, o0)
    ShadowHi1 = h1 - np.maximum(c1, o1)
    ShadowHi2 = h2 - np.maximum(c2, o2)
    ShadowHi3 = h3 - np.maximum(c3, o3)
    ShadowHi4 = h4 - np.maximum(c4, o4)

    ShadowLo = np.minimum(c0, o0) - l0
    ShadowLo1 = np.minimum(c1, o1) - l1
    ShadowLo2 = np.minimum(c2, o2) - l2
    ShadowLo3 = np.minimum(c3, o3) - l3
    ShadowLo4 = np.minimum(c4, o4) - l4

    if pattern_list[0] == "OnNeckBearish" and (
        BodyLength < 0
        and C_Body1 > 0
        and c1 < c0
        and c1 <= o0
        and c1 < (o0 - BodyLength * 0.5)
        and (l1 - c1) < BodyLength * 0.1
        and (c0 - c1) > BodyLength1 * 0.2
    ):
        return pattern_list[0]

    elif pattern_list[1] == "RisingWindowBullish" and (
        BodyLength < 0
        and C_Body1 > 0
        and c1 > o0
        and c1 > (o0 + BodyLength * 0.5)
        and c1 > (o1 + BodyLength1 * 0.1)
        and c1 < h1
        and o1 > c0
        and h1 > c0
    ):
        return pattern_list[1]

    # Add more pattern conditions here...

    else:
        return None