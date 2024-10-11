import unittest
from load_fact_leakage import Leakage
from pyspark.sql import SparkSession
from mock import MagicMock
from pyspark.sql.functions import Column, lit
from pyspark.sql.types import *

class TestSuiteOTC(unittest.TestCase):

    def setUp(self):
        self.spark = SparkSession.builder.enableHiveSupport().appName('test').getOrCreate()
        self.spark.sparkContext.setLogLevel("ERROR")
        self.spark.sql("use otc_dev_test_db")
        self.logger_obj = MagicMock()

    def type_cast_columns(self, df, cols_array, col_type):
        for colm in cols_array:
            df = df.withColumn(colm, df[colm].cast(col_type))
        return df

    def assertDataframesEqual(self, expected, result):
        """
        Assert that 2 dataframes contain the same data
        """
        difference_between_df = expected.subtract(result).union(result.subtract(expected)).take(1)
        if len(difference_between_df) != 0:
            print(difference_between_df, len(difference_between_df))
        return (True if len(difference_between_df) == 0 else False)
    
    def test_fact_leakage_columns(self):
        self.spark.sql("use otc_dev")
        result_df = self.spark.sql("select * from fact_leakage limit 5")
        expected_df = self.spark.read.options(header='True', inferSchema='True', delimiter=',').csv("/data/mondelez/publish/ptc/otc_analytics/process/tests/expected_df/facts/fact_leakage_schema_expected.csv")
        self.assertEqual(result_df.columns, expected_df.columns)
    
    def test_fact_leakage_column_types(self):
        self.spark.sql("use otc_dev")
        non_decimal_cols_arr = []
        decimal_columns = ["invoice_amount", "ar_amount", "discount_amount", "contract_compliance_leakage_amount", 
                            "pricing_error_leakage_amount", "unearned_leakage_amount", "billing_leakage_amount", 
                            "credit_notes_leakage_amount", "bad_debt_leakage_amount", 
                            "low_value_sweeps_leakage_amount", "invalid_deduction_leakage_amount"]
        result_df = self.spark.sql("select * from fact_leakage limit 5")
        result_df = result_df.select(decimal_columns)
        for name,colType in result_df.dtypes:
            if 'decimal' not in colType:
                non_decimal_cols_arr.append(name)

        self.assertTrue(True if len(non_decimal_cols_arr) == 0 else False)

    '''
    def test_fact_leakage(self):
        leakage_obj = Leakage(self.spark, self.logger_obj)
        result_df = leakage_obj.insert_into_fact("dim_finance_billing", "dim_delivery")
        expected_df = self.spark.read.options(header='True', inferSchema='True', delimiter=',').csv("/data/mondelez/publish/ptc/otc_analytics/process/tests/expected_df/facts/fact_leakage_expected.csv")
        
        # following columns are completely null in source code hence dropping them
        drop_columns = ("channel_code", "cash_discount_amount", "delay_time")
        result_df = result_df.drop(*drop_columns)
        expected_df = expected_df.drop(*drop_columns)

        # when amount columns are null in expected csv, spark reads them as string. And resultant null columns appear null. Hence convertig all to decimal.
        decimal_columns_conversion = ["invoice_amount", "ar_amount", "discount_amount", "contract_compliance_leakage_amount", 
                                    "pricing_error_leakage_amount", "unearned_leakage_amount", "billing_leakage_amount", 
                                    "credit_notes_leakage_amount", "bad_debt_leakage_amount", 
                                    "low_value_sweeps_leakage_amount", "invalid_deduction_leakage_amount"]
        result_df = self.type_cast_columns(result_df, decimal_columns_conversion, DecimalType(30,3))
        expected_df = self.type_cast_columns(expected_df, decimal_columns_conversion, DecimalType(30,3))

        # in source code these columns are sub-string of some column. Converting them to int for comparison
        int_columns_conversion = ["fiscal_period", "fiscal_year", "fiscal_month"]
        result_df = self.type_cast_columns(result_df, int_columns_conversion, IntegerType())

        # it is all number so expected csv reads as long. Converting result df column to long
        result_df = self.type_cast_columns(result_df, ["sales_document_number"], LongType())
        # expected csv reads it as timestamp
        expected_df = self.type_cast_columns(expected_df, ["load_date"], DateType())

        equal_result = self.assertDataframesEqual(expected_df, result_df)
        self.assertTrue(equal_result)
    '''

    def tearDown(self):
        self.spark.stop()
    
if __name__ == '__main__':
    unittest.main()
