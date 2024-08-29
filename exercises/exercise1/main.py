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
