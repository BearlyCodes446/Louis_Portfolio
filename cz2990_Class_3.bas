Attribute VB_Name = "Module1"
Option Explicit
Option Base 1

Function getBondPrice(ByVal y As Double, ByVal face As Double, ByVal couponRate As Double, _
                      ByVal m As Integer, Optional ByVal ppy As Integer = 1) As Double
    Dim nPeriods As Integer
    Dim r As Double
    Dim coupon As Double
    Dim cf As Double
    Dim total As Double
    Dim t As Integer

    nPeriods = m * ppy                  ' 10 or 20
    r = y / ppy                         ' rate per period
    coupon = face * couponRate / ppy    ' 80,000 or 40,000
    total = 0

    For t = 1 To nPeriods
        cf = coupon
        If t = nPeriods Then
            cf = cf + face              ' face value paid back at maturity
        End If
        total = total + cf * (1 + r) ^ (-t)
    Next t

    getBondPrice = total
End Function

Sub TestBondPrice()
    MsgBox Round(getBondPrice(0.03, 2000000, 0.04, 10, 1))   ' 2170604
    MsgBox Round(getBondPrice(0.03, 2000000, 0.04, 10, 2))   ' 2171686
End Sub


Function getBondDuration(ByVal y As Double, ByVal face As Double, _
                         ByVal couponRate As Double, ByVal m As Integer) As Double
    Dim coupon As Double
    Dim cf As Double
    Dim pvcf As Double
    Dim sumPvcf As Double
    Dim sumPvcfT As Double
    Dim t As Integer

    coupon = face * couponRate          ' 80,000 per year
    sumPvcf = 0
    sumPvcfT = 0

    For t = 1 To m
        cf = coupon
        If t = m Then
            cf = cf + face              ' face value paid back at maturity
        End If
        pvcf = cf * (1 + y) ^ (-t)      ' present value of this cash flow
        sumPvcf = sumPvcf + pvcf        ' bottom of the fraction (= bond price)
        sumPvcfT = sumPvcfT + pvcf * t  ' top of the fraction (time-weighted)
    Next t

    getBondDuration = sumPvcfT / sumPvcf
End Function

Sub TestBondDuration()
    MsgBox Round(getBondDuration(0.03, 2000000, 0.04, 10), 2)   ' 8.51
End Sub
