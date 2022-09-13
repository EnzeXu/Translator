from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.add_font('song', '', 'fonts/fireflysung.ttf', True)
        self.set_font('song', size=12)
        # # Calculate width of title and position
        # w = self.get_string_width(title) + 6
        # self.set_x((210 - w) / 2)
        # # Colors of frame, background and text
        # self.set_draw_color(0, 80, 180)
        # self.set_fill_color(230, 230, 0)
        # self.set_text_color(220, 50, 50)
        # # Thickness of frame (1 mm)
        # self.set_line_width(1)
        # # Title
        # self.cell(w, 9, title, 1, 1, 'C', 1)
        # # Line break
        # self.ln(10)
        pass

    def footer(self):
        pass
        # # Position at 1.5 cm from bottom
        # self.set_y(-15)
        # # Arial italic 8
        # # self.set_font('Arial', 'I', 8)
        # self.set_font('song', size=10)
        # # Text color in gray
        # self.set_text_color(128)
        # # Page number
        # self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, num, label):
        # Arial 12
        # self.set_font('Arial', '', 12)
        self.set_font('song', size=11)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        if len(label) > 0:
            self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, name):
        # Read text file
        # with open(name, 'rb') as fh:
        #     txt = fh.read().decode('latin-1')
        with open(name, 'r') as fh:
            txt = fh.readlines()
        txt = "".join(txt)
        # Times 12
        # self.set_font('Times', '', 12)
        self.set_font('song', size=11)
        # Output justified text
        self.multi_cell(0, 4, txt)
        # Line break
        self.ln()
        # Mention in italics
        # self.set_font('', 'I')
        self.set_font('song', size=11)
        # self.cell(0, 5, '(end of excerpt)')

    def print_chapter(self, num, title, name):
        self.add_page()
        self.set_font('Arial', 'B', 11)
        self.cell(0, 4, "Page {}".format(num))
        self.chapter_title(num, title)
        self.chapter_body(name)



if __name__ == "__main__":
    pdf = PDF()
    for i in range(392):
        pdf.print_chapter(i + 1, "", "pages/RM/page_{}.txt".format(i))
        print("pages/RM/page_{}.txt".format(i))
    pdf.output('test.pdf', 'F')
