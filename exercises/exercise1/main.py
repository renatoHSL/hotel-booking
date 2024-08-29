import pandas
from fpdf import FPDF

df = pandas.read_csv("articles.csv", dtype={"id": str})


class Article:
    def __init__(self, article_id):
        self.article_id = article_id
        self.name = df.loc[df["id"] == self.article_id, "name"].squeeze()

    def stock_update(self):
        current_stock = df.loc[df["id"] == self.article_id, "in stock"].squeeze()
        if current_stock > 0:
            df.loc[df["id"] == self.article_id, "in stock"] = current_stock - 1
            df.to_csv("articles.csv", index=False)
        else:
            print(f"{self.name} is out of stock!")


class ReceiptTicket:
    def __init__(self, article_id):
        self.article_id = article_id
        self.article_name = df.loc[df["id"] == self.article_id, "name"].squeeze()
        self.article_price = df.loc[df["id"] == self.article_id, "price"].squeeze()
        self.receipt_number = self.count_check()

    @staticmethod
    def count_check():
        with open("receipt_count.txt", "r+") as file:
            content = int(file.read())
            content += 1
            file.seek(0)
            file.write(str(content))
            file.truncate()
            return content

    def generate(self):
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Receipt nr.{self.receipt_number}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Article: {self.article_name}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Price: {self.article_price}", ln=1)

        pdf.output("receipt.pdf")


print(df)
article_ID = input("Choose an article to buy: ")
article = Article(article_ID)
receipt_ticket = ReceiptTicket(article_ID)
receipt_ticket.generate()
article.stock_update()


# Codigo com melhorias:
#
# import pandas as pd
# from fpdf import FPDF
#
#
# # Funções auxiliares para ler e salvar o CSV
# def load_articles(file_path="articles.csv"):
#     return pd.read_csv(file_path, dtype={"id": str})
#
#
# def save_articles(df, file_path="articles.csv"):
#     df.to_csv(file_path, index=False)
#
#
# class Article:
#     def __init__(self, article_id, df):
#         self.article_id = article_id
#         self.name = df.loc[df["id"] == self.article_id, "name"].squeeze()
#         self.stock = df.loc[df["id"] == self.article_id, "in stock"].squeeze()
#         self.price = df.loc[df["id"] == self.article_id, "price"].squeeze()
#
#     def is_in_stock(self):
#         return self.stock > 0
#
#     def reduce_stock(self, amount=1):
#         if self.is_in_stock():
#             self.stock -= amount
#             return True
#         else:
#             print(f"{self.name} is out of stock!")
#             return False
#
#     def update_stock_in_df(self, df):
#         df.loc[df["id"] == self.article_id, "in stock"] = self.stock
#
#
# class ReceiptTicket:
#     def __init__(self, article):
#         self.article = article
#         self.receipt_number = self._increment_receipt_count()
#
#     @staticmethod
#     def _increment_receipt_count():
#         try:
#             with open("receipt_count.txt", "r+") as file:
#                 content = int(file.read())
#                 content += 1
#                 file.seek(0)
#                 file.write(str(content))
#                 file.truncate()
#                 return content
#         except FileNotFoundError:
#             with open("receipt_count.txt", "w") as file:
#                 file.write("1")
#             return 1
#
#     def generate(self, file_name="receipt.pdf"):
#         pdf = FPDF(orientation="P", unit="mm", format="A4")
#         pdf.add_page()
#
#         pdf.set_font(family="Times", size=16, style="B")
#         pdf.cell(w=50, h=8, txt=f"Receipt nr.{self.receipt_number}", ln=1)
#
#         pdf.set_font(family="Times", size=16, style="B")
#         pdf.cell(w=50, h=8, txt=f"Article: {self.article.name}", ln=1)
#
#         pdf.set_font(family="Times", size=16, style="B")
#         pdf.cell(w=50, h=8, txt=f"Price: {self.article.price}", ln=1)
#
#         pdf.output(file_name)
#         print(f"Receipt generated: {file_name}")
#
#
# # Main program
# df = load_articles()
# print(df)
#
# article_ID = input("Choose an article to buy: ")
# article = Article(article_ID, df)
#
# if article.is_in_stock():
#     receipt_ticket = ReceiptTicket(article)
#     receipt_ticket.generate(f"receipt_{article_ID}.pdf")
#     if article.reduce_stock():
#         article.update_stock_in_df(df)
#         save_articles(df)
# else:
#     print(f"Sorry, {article.name} is not available.")
