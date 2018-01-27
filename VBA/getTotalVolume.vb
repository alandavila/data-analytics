Sub getStockVolume()
    Dim last_row As Long
    Dim cur_row As Long
    Dim cur_total_row As Integer
    Dim cur_total As Double
    Dim cur_ticker As String
    Dim open_value As Double
    Dim close_value As Double
    Dim greatest_volume As Double
    Dim greatest_vol_ticker As String
    Dim greatest_inc As Double
    Dim greatest_inc_ticker As String
    Dim greatest_dec As Double
    Dim greatest_dec_ticker As String
    Dim open_value_found As Boolean
    
    'Filling headers and titles
    Range("P1").Value = "Ticker"
    Range("Q1").Value = "Value"
    Range("O2").Value = "Greatest % Increase"
    Range("O3").Value = "Greatest % Decrease"
    Range("O4").Value = "Greatest Total Volume"
    
    cur_total_row = 2
    cur_total = 0
    cur_ticker = Cells(2, 1).Value
    open_value = Cells(2, 3).Value
    last_row = Cells(1, 1).End(xlDown).Row

    'Loop over all rows with data
    For cur_row = 2 To last_row
        'Determine when we reach a new ticker
        If Cells(cur_row, 1) <> cur_ticker Then
            'Next open value might not be in the first row of next ticker
            open_value_found = False
            'Get delta between previous ticker's closing and openning values
            Cells(cur_total_row, 10).Value = close_value - open_value
            'Get previous ticker's total value
            Cells(cur_total_row, 12).Value = cur_total
            'Compare previous ticker's total value with the max found so far
            'Update greatet volume if current is new max
            If cur_total > greatest_volume Then
                greatest_volume = cur_total
                greatest_vol_ticker = cur_ticker
            End If
            'Fill previour ticker totals: ticker, percentage change
            Cells(cur_total_row, 9).Value = cur_ticker
            Cells(cur_total_row, 11).Value = (close_value - open_value) / open_value
            Cells(cur_total_row, 11).NumberFormat = "0.00%"
            'Color cell red if percentage cell is negative, green otherwise
            If Cells(cur_total_row, 10).Value > 0 Then
                Cells(cur_total_row, 10).Interior.ColorIndex = 4
            Else
                Cells(cur_total_row, 10).Interior.ColorIndex = 3
            End If
            'Update greatest increas/decrease if current is new max
            If Cells(cur_total_row, 11).Value > greatest_inc Then
                greatest_inc = Cells(cur_total_row, 11).Value
                greatest_inc_ticker = cur_ticker
            End If
            If Cells(cur_total_row, 11).Value < greatest_dec Then
                greatest_dec = Cells(cur_total_row, 11).Value
                greatest_dec_ticker = cur_ticker
            End If
            'Reset current variables to start aggregating values for next ticker
            cur_total = 0
            cur_total_row = cur_total_row + 1
            cur_ticker = Cells(cur_row, 1)
            open_value = Cells(cur_row, 3).Value
            'Check for open value and make sure it is not zero in current row
            If open_value > 0 Then
                open_value_found = True
            End If
        End If
        'Start aggregating values for the current ticker
        cur_total = cur_total + Cells(cur_row, 7).Value
        close_value = Cells(cur_row, 6).Value
        open_value = Cells(cur_row, 3).Value
        'Make a note when/if open value is not zero in open_value_found
        If Not open_value_found And open_value > 0 Then
            open_value = Cells(cur_row, 3).Value
            open_value_found = True
        End If
    Next cur_row
    'Fill aggregated findings in corresponding cells
    Cells(4, 17).Value = greatest_volume
    Cells(4, 16).Value = greatest_vol_ticker
    Cells(2, 17).Value = greatest_inc
    Cells(2, 16).Value = greatest_inc_ticker
    Cells(3, 17).Value = greatest_dec
    Cells(3, 16).Value = greatest_dec_ticker
End Sub
'Routing to apply getStockVolume function in all worksheets one by one
Sub apply_on_sheets()

     Dim count As Integer
     
     count = ActiveWorkbook.Worksheets.count
     For current = 1 To count
        MsgBox (ActiveWorkbook.Worksheets(current).Name)
        ActiveWorkbook.Worksheets(current).Select
        getStockVolume
     Next current

End Sub