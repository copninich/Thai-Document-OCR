# coding: utf-8
from PIL import Image , ImageGrab
import pytesseract
from matplotlib import pyplot as plt
import numpy as np
import difflib
import pandas as pd
from ssg import syllable_tokenize
from pythainlp.tokenize import word_tokenize


def compare_diff(df, easy_wrong: str, answer: str):
    df = df.copy()
    df['add'] = ''  
    df['delete'] = ''  
    df['correct word str'] = text
    df['OCR str'] = ocr
    for index, row in df.iterrows():  # iterate through each row
        a = row[easy_wrong]  # ocr engine's output
        b = row[answer]  # answer
       
        add_list = []
        delete_list = []
        for i,s in enumerate(difflib.ndiff(a, b)):  # iterate through the differences
            if s[0]==' ': continue
            elif s[0]=='-':  # characters that need to be del to match str
                delete_list.append(s[-1])
            elif s[0]=='+':  # characters that need to be add to match str
                add_list.append(s[-1])
        if len(delete_list) > 0:
            df.loc[index, 'delete'] = "|".join(delete_list)
        if len(add_list) > 0:
            df.loc[index, 'add'] = "|".join(add_list)
        add_text = len(add_list)
        del_text = len(delete_list)
        print("Add Text = {} | Delete Text = {}".format(add_text,del_text))

        #character error rate calculate for test OCR lib
        I = add_text
        D = del_text
        S = 0
        N = ocr
        CER = (I+D+S)/N

       # print error rate
        print('Character Error Rate = {}'.format(CER))

        #print example data in csv file
        print(df)
    df['CER Value'] = CER
    return df

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if __name__ == "__main__":
    listfile = [("small_text.png","คําสั่งโรงเรียนยุพราชวิทยาลัย ที่ 0552/2563"),
        ("01.jpg","คําสั่งโรงเรียนยุพราชวิทยาลัยที่ 0552/2563 เรื่อง แต่งตั้งคณะกรรมการดําเนินการสอบปลายภาคเรียนที่ 1 ประจําปีการศึกษา 2563 ด้วยโรงเรียนยุพราชวิทยาลัย จังหวัดเชียงใหม่ ได้กําหนดให้มีการจัดสอบปลายภาคเรียนที่ 1 ประจําปีการศึกษา 2563 ในระดับชั้นมัธยมศึกษาปีที่ 1 - 6 ระหว่างวันที่ 9 - 13 พฤศจิกายน พ.ศ. 2563 เพื่อให้ การจัดการสอบเป็นไปด้วยความเรียบร้อย มีประสิทธิภาพ และเป็นไปตามวัตถุประสงค์ของการจัดสอบ อาศัย อํานาจตามพระราชบัญญัติระเบียบข้าราชการครูและบุคลากรทางการศึกษา พุทธศักราช 2547 แก้ไขเพิ่มเติม (ฉบับที่ 3) พุทธศักราช 2553 มาตรา 27 จึงแต่งตั้งคณะกรรมการดําเนินการสอบ เพื่อปฏิบัติงานในหน้าที่ต่างๆดังนี้ 1. คณะกรรมการฝ่ายอํานวยการสนามสอบ ประกอบด้วย 1.1 นายฐิตติณัฐ ศักดิ์ธนานนท์ ประธานกรรมการ 1.2 นายธนัฏฐ์ แสนแปง กรรมการ 1.3 นายธนพล กมลหัตถ์ กรรมการ 1.4 นายนิกร ทวีเดช กรรมการ 1.5 นายสมบัติ คําบุญสูง กรรมการและเลขานุการ หน้าที่ วางแผน กํากับดูแลการสอบ ให้เป็นไปด้วยความเรียบร้อย 2. คณะกรรมการฝ่ายอาคารสถานที่ ประกอบด้วย 2.1 นายธนัฏฐ์ แสนแปงประธานกรรมการ 2.2 นายกิตติพงศ์ ยอดชุมภู รองประธานกรรมการ 2.3 นักการภารโรงและแม่บ้านทุกคน กรรมการ 2.4 นายเจษฎา เจริญชัยชนะ กรรมการและเลขานุการ หน้าที่ จัดเตรียมห้องสอบ จํานวนที่นั่งสอบให้เพียงพอในการสอบแต่ละอาคารก่อนการสอบล่วงหน้า 1 วัน จัดห้องสอบห้องละ 36 ที่นั่งสอบ โดยจัดแบบ 6x6"),
        ("02.jpg","๑. คณะกรรมการบริหารโรงเรียน นายฐิตติณัฐ ศักดิ์ธนานนท์ ผู้อํานวยการโรงเรียน ประธานกรรมการ นายธนัฏฐ์ แสนแปง รองผู้อํานวยการฝ่ายอํานวยการ รองประธานกรรมการ นายสมบัติ คําบุญสูง รองผู้อํานวยการฝ่ายจัดการศึกษา กรรมการ นายธนพล กมลหัตถ์ รองผู้อํานวยการฝ่ายบริหารทั่วไป กรรมการ นายนิกร ทวีเดช รองผู้อํานวยการฝ่ายกิจการนักเรียน กรรมการ นางผกาพรรณ พรหมมานุวัติ ปฏิบัติหน้าที่รองผู้อํานวยการฝ่ายนโยบายและแผน กรรมการ นายกิตติพงศ์ ยอดชุมภู ผู้ช่วยผู้อํานวยการฝ่ายบริหารทั่วไป กรรมการ นางสุกาญจน์ดา สิงฆราช ผู้ช่วยผู้อํานวยการฝ่ายกิจการนักเรียน กรรมการ นางวัชราพร ฉลาด ผู้ช่วยผู้อํานวยการฝ่ายจัดการศึกษา กรรมการ นายธีรวัฒน์ บุญทวี ผู้ช่วยผู้อํานวยการฝ่ายนโยบายและแผน กรรมการ นายสราญ คําอ้าย หัวหน้ากลุ่มสาระการเรียนรู้ภาษาไทย กรรมการ นางสุภารัตน์ คากิซากิ หัวหน้ากลุ่มสาระการเรียนรู้สังคมศึกษา ศาสนา และวัฒนธรรม กรรมการ นางศิริพร สายสอน หัวหน้ากลุ่มสาระการเรียนรู้การงานอาชีพและเทคโนโลยี กรรมการ นายวรมงคล ภาพพริ้ง หัวหน้ากลุ่มกิจกรรมพัฒนาผู้เรียน กรรมการ นายนิโรจน์ แก้วชะเนตร หัวหน้ากลุ่มสาระการเรียนรู้วิทยาศาสตร์ กรรมการ นางน้ำฝน โทปุญญานนท์ หัวหน้ากลุ่มสาระการเรียนรู้ภาษาต่างประเทศ ก กรรมการ นางไพริน นันทะเสน หัวหน้ากลุ่มสาระการเรียนรู้ภาษาต่างประเทศ ข กรรมการ นางจารุวรรณ ศริจันทร์ หัวหน้ากลุ่มสาระการเรียนรู้คณิตศาสตร์ กรรมการ นายทศพล สุภาหาญ หัวหน้ากลุ่มสาระการเรียนรู้สุขศึกษาและพลศึกษา กรรมการ นางเสาวนีย์ พงษ์ปิณฑะดิษ หัวหน้ากลุ่มสาระการเรียนรู้ศิลปะ กรรมการ"),
        ("03.png","คําสั่งโรงเรียนยุพราชวิทยาลัย ที่ ๐๑๗๔/๒๕๖๒ เรื่อง แต่งตั้งบุคลากรปฏิบัติหน้าที่ตามโครงสร้างการบริหารงานโรงเรียนยุพราชวิทยาลัย ปีการศึกษา ๒๕๖๒ โรงเรียนยุพราชวิทยาลัย ได้ดําเนินการจัดการศึกษาของโรงเรียนตามโครงสร้างการบริหารงานของโรงเรียน ซึ่งประกอบด้วยคณะกรรมการดําเนินงานฝ่ายต่าง ๆ เพื่อให้การดําเนินงานเป็นไปด้วยความเรียบร้อย ถูกต้อง รวดเร็ว มีประสิทธิภาพและเกิดประสิทธิผล อาศัยอํานาจตามพระราชบัญญัติระเบียบบริหารข้าราชการครูแล บุคลากรทางการ ศึกษา พุทธศักราช ๒๕๕๗ มาตรา ๒๗ และอาศัยอํานาจตามคําสั่งสํานักงานคณะกรรมการการศึกษาขั้นพื้นฐานที่ ๓๐๙/ ๒๕๕๐ ลงวันที่ ๒ กุมภาพันธ์ ๒๕๕๐ เรื่องการมอบอํานาจการปฏิบัติราชการแทนเกี่ยวกับข้าราชการและลูกจ้างประจํา จึงแต่งตั้งข้าราชการครูและบุคลากรทางการศึกษาปฏิบัติหน้าที่ตามโครงสร้างและพรรณนางานของโรงเรียน ภาคเรียน ที่ ๒ ประจําปีการศึกษา ๒๕๖๐"),
        ("04.jpg","3. คณะกรรมการจัดทําข้อสอบและส่งข้อสอบ ประกอบด้วย 3.1 นายสราญ คําอ้าย ประธานกรรมการ 3.2 นายธีรวัฒน์ บุญทวี กรรมการ 3.3 นางบุปผา ธนะชัยขันธ์ กรรมการ 3.4 นายพัทธยากร บุสสยา กรรมการ 3.5 ครูผู้สอนในรายวิชาที่มีการจัดสอบปลายภาค กรรมการ 3.6 นายพรศักดิ์ สุทธยากร กรรมการ 3.7 นายมนู กันทะวงค์ กรรมการและเลขานุการ หน้าที่ 1. รับผิดชอบออกข้อสอบ จัดพิมพ์ข้อสอบ และส่งข้อสอบที่บรรจุซองเรียบร้อยแล้วที่ห้องศูนย์สอบ ภายในวันศุกร์ที่ 6 พฤศจิกายน พ.ศ. 2563 ก่อนเวลา 12.00 น. 2. จัดทําสําเนาข้อสอบ และเอกสารอื่น ๆ ที่เกี่ยวข้องกับการสอบปลายภาคเรียน 4. คณะกรรมการฝ่ายรับ - จ่ายข้อสอบ ประกอบด้วย 4.1 นายสราญ คําอ้าย ประธานกรรมการ 4.2 นายธีรวัฒน์ บุญทวี กรรมการ 4.3 นักศึกษาฝึกประสบการณ์วิชาชีพครูประจําอาคาร กรรมการ 4.4 นายมนู กันทะวงค์ กรรมการและเลขานุการ หน้าที่ รับ - จ่ายข้อสอบ ตามอาคารและเวลาดังต่อไปนี้ ภาคเช้า - เวลา 07.45 น. รับข้อสอบจากกองกลางห้องศูนย์สอบ (อาคาร 2) เพื่อนําไปส่งกองกลาง ประจําอาคาร - เวลา 11.45 น. รับข้อสอบที่สอบแล้วจากกรรมการกลางประจําอาคาร เพื่อนําไปส่งกองกลางห้องศูนย์สอบ (อาคาร 2) ภาคบ่าย - เวลา 12.00 น. รับข้อสอบจากกองกลางห้องศูนย์สอบ (อาคาร 2) เพื่อนําไปส่งกองกลาง ประจําอาคาร เวลา 15.45 น. รับข้อสอบที่สอบแล้วจากกรรมการกลางประจําอาคาร เพื่อนําไปส่ง กองกลางห้องศูนย์สอบ (อาคาร 2) หมายเหตุ อุปกรณ์การสอบรับจากห้องศูนย์สอบวันแรก และส่งคืนวันสุดท้ายของการสอบ 4. คณะกรรมการกลางประจําศูนย์สอบ 4.1 อาคาร 2 (เรือนวิเชียร) กองกลางสนามสอบ สํานักงานอยู่ที่ห้องศูนย์สอบ อาคาร 2 ประกอบด้วย 4.1.1 นายสราญ คําอ้าย ประธานกรรมการ 4.1.2 นายมนู กันทะวงค์ กรรมการ 4.1.3 นายธีรวัฒน์ บุญทวี กรรมการ"),
        ("05.jpg","4.1.4 นางขนิษฐา คมขํา กรรมการ 4.1.5 นายพัทธยากร บุสสยา กรรมการ 4.1.6 นักศึกษาฝึกประสบการณ์วิชาชีพครูประจําอาคาร กรรมการ 4.1.7 นางบุปผา ธนะชัยขันธ์ กรรมการและเลขานุการ หน้าที่ 1. จัดอุปกรณ์ต่าง ๆ เกี่ยวกับการสอบ สําหรับจ่ายให้กรรมการกลางประจําอาคาร 2. เก็บรักษาข้อสอบทุกวิชาและจ่ายให้กรรมการกลางประจําอาคารเป็นรายวันเพื่อนําไปจัดสอบ ในแต่ละอาคาร 3. เก็บรักษากระดาษคําตอบทุกรายวิชาที่สอบเสร็จแล้วจากการนําส่งของกรรมการกลางประจํา อาคารในแต่ละวัน 4. ให้ครูประจําวิชารับกระดาษคําตอบที่สอบเสร็จเพื่อนําไปตรวจให้คะแนน โดย - วิชาที่สอบภาคเช้ารับ ในช่วงเวลา 13.30 - 16.00 น. - วิชาที่สอบภาคบ่ายรับ ในช่วงเวลา 08.30 - 12.00 น. ของวันถัดไป เว้นวันหยุดราชการ 5. รับและรวบรวมอุปกรณ์ต่าง ๆ เกี่ยวกับการสอบคืนจากกรรมการกลางประจําอาคาร 6. ประสานงานกับกรรมการกลางประจําอาคารในการแก้ไขปัญหาต่าง ๆ เกี่ยวกับการสอบ 7. ควบคุมการปฏิบัติงานของนักศึกษาฝึกประสบการณ์ในการรับ - ส่งข้อสอบไปยังอาคารต่าง ๆ 8. งานอื่น ๆ ตามที่ได้รับมอบหมาย 4.2 กรรมการกลางประจําอาคาร 4.2.1 อาคาร 3 (อาคารเรือนรัตน) สํานักงานอยู่ที่ชั้น 2 ห้องปฏิบัติการ 324 (วิทยาศาสตร์ ม.1) คณะกรรมการ ประกอบด้วย 4.2.1.1 นางสาววราภรณ์ เป้ามณี 4.2.1.2 นางนิตยา ศรีสุวรรณ์ 4.2.1.3 นักศึกษาฝึกประสบการณ์ประจําอาคาร 4.2.2 อาคาร 5 (อาคารเรือนวชิระ) สํานักงานอยู่ที่ชั้น 2 ห้องทะเบียนวัดผล คณะกรรมการ ประกอบด้วย 4.2.2.1 นางสาวอัญภัทร บุตรพรหม 4.2.2.2 นางสาวกัญปภัสร์ คําป้อ 4.2.2.3 นักศึกษาฝึกประสบการณ์ประจําอาคาร 4.2.3 อาคาร 7 (เรือนรัตนมณี) สํานักงานอยู่ที่ชั้น 2 ห้องศูนย์การเรียนรู้สังคมศึกษา คณะกรรมการ ประกอบด้วย 4.2.3.1 นายทวี ฤทธิเดช 4.2.3.2 นายกิตติพงศ์ ยอดชุมภู 4.2.3.3 นักศึกษาฝึกประสบการณ์ประจําอาคาร"),
        ("06.jpg","4.2.4 อาคาร 8 (เรือนศรีมรกต) สํานักงานอยู่ที่ชั้น 2 ห้องศูนย์การเรียนรู้ภาษาไทย คณะกรรมการ ประกอบด้วย 4.2.4.1 นางกิ่งดาว จองบุ๊ก 4.2.4.2 นางสาวมัณฑลี จิตเจนสุวรรณ 4.2.4.3 นักศึกษาฝึกประสบการณ์ประจําอาคาร 4.2.5 อาคาร 10 (อาคารเพชรรัตน์) สํานักงานอยู่ที่ชั้น 2 ห้องคอมพิวเตอร์ (1023) คณะกรรมการ ประกอบด้วย 4.2.5.1 นายปณวรรต บุญตาศานย์ 4.2.5.2 นางสาวหทัยรัตน์ ศรีวิโรจน์ 4.2.5.3 นักศึกษาฝึกประสบการณ์ประจําอาคาร 4.2.6 อาคาร 12 (อาคารวชิรดารา) สํานักงานอยู่ที่ชั้น 3 ห้องศูนย์การเรียนรู้คณิตศาสตร์ (1231) คณะกรรมการ ประกอบด้วย 4.2.6.1 นางจารุวรรณ ศรีจันทร์ 4.2.6.2 นาง ณ ชนก ปาลี 4.2.6.3 นางสาวสุภาสินี เสวันตุ่น 4.2.6.4 นักศึกษาฝึกประสบการณ์ประจําอาคาร หน้าที่ 1. วางแผนจัดการดําเนินการสอบในอาคารให้เป็นไปด้วยความเรียบร้อยตามระเบียบการสอบของ ทางราชการ 2. จัดระบบการรับ - ส่งข้อสอบทุกรายวิชาของแต่ละวันเพื่อนําไปดําเนินการสอบให้เป็นไปตามตารางสอบ 3. ภายหลังการสอบเสร็จในแต่ละวันให้นําข้อสอบและกระดาษคําตอบส่งคืนกรรมการกลางโดยส่งวันละ 2 ครั้ง คือ ภาคเช้าและภาคบ่าย โดยมีนักศึกษาฝึกประสบการณ์ประจําอาคารเป็นผู้ดําเนินการ 4. สรุปบัญชีรับ - ส่งข้อสอบ และกระดาษคําตอบภายในอาคารที่รับผิดชอบ ส่งคืนพร้อมข้อสอบ) 5. ประสานงานกับรองผู้อํานวยการฝ่ายจัดการศึกษาและกรรมการกลางเพื่อแก้ไขปัญหาต่าง ๆ เกี่ยวกับการสอบ 6. วันสุดท้ายของการสอบ ให้รวบรวมอุปกรณ์การสอบทุกชนิดส่งคืนกรรมการกลาง 7. ควบคุมดูแลการปฏิบัติงานของนักศึกษาฝึกประสบการณ์ประจําอาคาร 8. งานอื่น ๆ ตามที่ได้รับมอบหมาย"),
        ("07.jpg","ด้วย โรงเรียนยุพราชวิทยาลัย กําหนดสอบคัดเลือกนักเรียนระดับชั้นมัธยมศึกษาปีที่ ๑ และ ระดับชั้นมัธยมศึกษาปีที่ ๔ ประเภทโครงการเรียนดี ประจําปีการศึกษา ๒๕๖๔ ในวันที่ ๑๐-๑๑ ตุลาคม ๒๕๖๓ นั้น เพื่อให้การดําเนินการภารกิจด้านต่าง ๆ ของการสอบคัดเลือกนักเรียนเป็นไปด้วยความเรียบร้อย บริสุทธิ์ ยุติธรรม มีประสิทธิภาพ และเป็นไปตามวัตถุประสงค์ สอดคล้องกับนโยบายและแนวปฏิบัติเกี่ยวกับ การรับนักเรียน โดยอาศัยอํานาจตามพระราชบัญญัติระเบียบบริหารข้าราชการครูและบุคลากรทางการศึกษา พุทธศักราช ๒๕๕๗ มาตรา ๒๗ และอาศัยอํานาจตามคําสั่งสํานักงานคณะกรรมการการศึกษาขั้นพื้นฐานที่ ๑๐๙/๒๕๕๐ ลงวันที่ ๒ กุมภาพันธ์ ๒๕๕๐ เรื่อง การมอบอํานาจ การบังคับบัญชาข้าราชการและลูกจ้าง จึงแต่งตั้งคณะกรรมการดําเนินงานเพื่อปฏิบัติงานในหน้าที่ต่าง ๆ ดังนี้"),
        ("08.jpg","(นายฐิตติณัฐ ศักดิ์ธนานนท์) ผู้อํานวยการโรงเรียนยุพราชวิทยาลัย"),
        ("09.jpg","อังรีดูนังต์ปราจีนบุรีพ่อค้าซัพพลายเออร์ ปทุมธานีน้อยแอ๊บแบ๊วเคลียร์ ซัพพลายสะกอมบ ลอนด์ อุทัยธานีผู้นําวอลนัต เอ็มโพเรียมเซ็กแจ็ส แคปซิงอโยธยาธนบุรีผลักดัน ขอนแก่น ประจวบคีรีขันธ์ผลักดันพัทลุงอุบลราชธานี โบตั๋น กําแพงเพชรเอเพรสโซผลักดัน สหัสวรรษ ว้อยไฟลท์แรลลี่เที่ยงคืน แอปเปิ้ลมหาสารคามโบรกเกอร์โรลออน ซิม มอบตัวอะสไลด์สต๊อค บอยคอตต์เลยไฮเปอร์พ่อค้า นครสวรรค์อิสรชนใช้งานคาเฟ เพชรบุรี"),
        ("12.jpg","หน้าที่ ๑. ออกข้อสอบคัดเลือกนักเรียนเข้าเรียนต่อระดับชั้นมัธยมศึกษาปีที่ ๑ และระดับชั้นมัธยมศึกษาปีที่ ๔ ประเภทโครงการเรียนดี ประจําปีการศึกษา ๒๕๖๔ ๒. ปฏิบัติภารกิจโดยเคร่งครัดและให้ถือเป็นความลับของทางราชการห้ามเปิดเผย ๓. งานอื่น ๆ ตามที่ได้รับมอบหมาย ให้คณะกรรมการที่ได้รับการแต่งตั้งทุกท่านปฏิบัติหน้าที่ด้วยความรับผิดชอบ และเต็มความสามารถ เพื่อประโยชน์สูงสุดของทางราชการ"),
        ("13.jpg","หน้าที่ ให้นโยบายและคําปรึกษา สนับสนุนอํานวยความสะดวก กํากับดูแล และช่วยแก้ปัญหาต่าง ๆ ให้การดําเนินงานสําเร็จตามวัตถุประสงค์"),
        ("01_re.jpg","คําสั่งโรงเรียนยุพราชวิทยาลัยที่ 0552/2563 เรื่อง แต่งตั้งคณะกรรมการดําเนินการสอบปลายภาคเรียนที่ 1 ประจําปีการศึกษา 2563 ด้วยโรงเรียนยุพราชวิทยาลัย จังหวัดเชียงใหม่ ได้กําหนดให้มีการจัดสอบปลายภาคเรียนที่ 1 ประจําปีการศึกษา 2563 ในระดับชั้นมัธยมศึกษาปีที่ 1 - 6 ระหว่างวันที่ 9 - 13 พฤศจิกายน พ.ศ. 2563 เพื่อให้ การจัดการสอบเป็นไปด้วยความเรียบร้อย มีประสิทธิภาพ และเป็นไปตามวัตถุประสงค์ของการจัดสอบ อาศัย อํานาจตามพระราชบัญญัติระเบียบข้าราชการครูและบุคลากรทางการศึกษา พุทธศักราช 2547 แก้ไขเพิ่มเติม (ฉบับที่ 3) พุทธศักราช 2553 มาตรา 27 จึงแต่งตั้งคณะกรรมการดําเนินการสอบ เพื่อปฏิบัติงานในหน้าที่ต่างๆดังนี้ 1. คณะกรรมการฝ่ายอํานวยการสนามสอบ ประกอบด้วย 1.1 นายฐิตติณัฐ ศักดิ์ธนานนท์ ประธานกรรมการ 1.2 นายธนัฏฐ์ แสนแปง กรรมการ 1.3 นายธนพล กมลหัตถ์ กรรมการ 1.4 นายนิกร ทวีเดช กรรมการ 1.5 นายสมบัติ คําบุญสูง กรรมการและเลขานุการ หน้าที่ วางแผน กํากับดูแลการสอบ ให้เป็นไปด้วยความเรียบร้อย 2. คณะกรรมการฝ่ายอาคารสถานที่ ประกอบด้วย 2.1 นายธนัฏฐ์ แสนแปงประธานกรรมการ 2.2 นายกิตติพงศ์ ยอดชุมภู รองประธานกรรมการ 2.3 นักการภารโรงและแม่บ้านทุกคน กรรมการ 2.4 นายเจษฎา เจริญชัยชนะ กรรมการและเลขานุการ หน้าที่ จัดเตรียมห้องสอบ จํานวนที่นั่งสอบให้เพียงพอในการสอบแต่ละอาคารก่อนการสอบล่วงหน้า 1 วัน จัดห้องสอบห้องละ 36 ที่นั่งสอบ โดยจัดแบบ 6x6"),
        ("02_re.jpg","๑. คณะกรรมการบริหารโรงเรียน นายฐิตติณัฐ ศักดิ์ธนานนท์ ผู้อํานวยการโรงเรียน ประธานกรรมการ นายธนัฏฐ์ แสนแปง รองผู้อํานวยการฝ่ายอํานวยการ รองประธานกรรมการ นายสมบัติ คําบุญสูง รองผู้อํานวยการฝ่ายจัดการศึกษา กรรมการ นายธนพล กมลหัตถ์ รองผู้อํานวยการฝ่ายบริหารทั่วไป กรรมการ นายนิกร ทวีเดช รองผู้อํานวยการฝ่ายกิจการนักเรียน กรรมการ นางผกาพรรณ พรหมมานุวัติ ปฏิบัติหน้าที่รองผู้อํานวยการฝ่ายนโยบายและแผน กรรมการ นายกิตติพงศ์ ยอดชุมภู ผู้ช่วยผู้อํานวยการฝ่ายบริหารทั่วไป กรรมการ นางสุกาญจน์ดา สิงฆราช ผู้ช่วยผู้อํานวยการฝ่ายกิจการนักเรียน กรรมการ นางวัชราพร ฉลาด ผู้ช่วยผู้อํานวยการฝ่ายจัดการศึกษา กรรมการ นายธีรวัฒน์ บุญทวี ผู้ช่วยผู้อํานวยการฝ่ายนโยบายและแผน กรรมการ นายสราญ คําอ้าย หัวหน้ากลุ่มสาระการเรียนรู้ภาษาไทย กรรมการ นางสุภารัตน์ คากิซากิ หัวหน้ากลุ่มสาระการเรียนรู้สังคมศึกษา ศาสนา และวัฒนธรรม กรรมการ นางศิริพร สายสอน หัวหน้ากลุ่มสาระการเรียนรู้การงานอาชีพและเทคโนโลยี กรรมการ นายวรมงคล ภาพพริ้ง หัวหน้ากลุ่มกิจกรรมพัฒนาผู้เรียน กรรมการ นายนิโรจน์ แก้วชะเนตร หัวหน้ากลุ่มสาระการเรียนรู้วิทยาศาสตร์ กรรมการ นางน้ำฝน โทปุญญานนท์ หัวหน้ากลุ่มสาระการเรียนรู้ภาษาต่างประเทศ ก กรรมการ นางไพริน นันทะเสน หัวหน้ากลุ่มสาระการเรียนรู้ภาษาต่างประเทศ ข กรรมการ นางจารุวรรณ ศริจันทร์ หัวหน้ากลุ่มสาระการเรียนรู้คณิตศาสตร์ กรรมการ นายทศพล สุภาหาญ หัวหน้ากลุ่มสาระการเรียนรู้สุขศึกษาและพลศึกษา กรรมการ นางเสาวนีย์ พงษ์ปิณฑะดิษ หัวหน้ากลุ่มสาระการเรียนรู้ศิลปะ กรรมการ"),
        ("03_re.png","คําสั่งโรงเรียนยุพราชวิทยาลัย ที่ ๐๑๗๔/๒๕๖๒ เรื่อง แต่งตั้งบุคลากรปฏิบัติหน้าที่ตามโครงสร้างการบริหารงานโรงเรียนยุพราชวิทยาลัย ปีการศึกษา ๒๕๖๒ โรงเรียนยุพราชวิทยาลัย ได้ดําเนินการจัดการศึกษาของโรงเรียนตามโครงสร้างการบริหารงานของโรงเรียน ซึ่งประกอบด้วยคณะกรรมการดําเนินงานฝ่ายต่าง ๆ เพื่อให้การดําเนินงานเป็นไปด้วยความเรียบร้อย ถูกต้อง รวดเร็ว มีประสิทธิภาพและเกิดประสิทธิผล อาศัยอํานาจตามพระราชบัญญัติระเบียบบริหารข้าราชการครูแล บุคลากรทางการ ศึกษา พุทธศักราช ๒๕๕๗ มาตรา ๒๗ และอาศัยอํานาจตามคําสั่งสํานักงานคณะกรรมการการศึกษาขั้นพื้นฐานที่ ๓๐๙/ ๒๕๕๐ ลงวันที่ ๒ กุมภาพันธ์ ๒๕๕๐ เรื่องการมอบอํานาจการปฏิบัติราชการแทนเกี่ยวกับข้าราชการและลูกจ้างประจํา จึงแต่งตั้งข้าราชการครูและบุคลากรทางการศึกษาปฏิบัติหน้าที่ตามโครงสร้างและพรรณนางานของโรงเรียน ภาคเรียน ที่ ๒ ประจําปีการศึกษา ๒๕๖๐"),
        ("04_re.jpg","3. คณะกรรมการจัดทําข้อสอบและส่งข้อสอบ ประกอบด้วย 3.1 นายสราญ คําอ้าย ประธานกรรมการ 3.2 นายธีรวัฒน์ บุญทวี กรรมการ 3.3 นางบุปผา ธนะชัยขันธ์ กรรมการ 3.4 นายพัทธยากร บุสสยา กรรมการ 3.5 ครูผู้สอนในรายวิชาที่มีการจัดสอบปลายภาค กรรมการ 3.6 นายพรศักดิ์ สุทธยากร กรรมการ 3.7 นายมนู กันทะวงค์ กรรมการและเลขานุการ หน้าที่ 1. รับผิดชอบออกข้อสอบ จัดพิมพ์ข้อสอบ และส่งข้อสอบที่บรรจุซองเรียบร้อยแล้วที่ห้องศูนย์สอบ ภายในวันศุกร์ที่ 6 พฤศจิกายน พ.ศ. 2563 ก่อนเวลา 12.00 น. 2. จัดทําสําเนาข้อสอบ และเอกสารอื่น ๆ ที่เกี่ยวข้องกับการสอบปลายภาคเรียน 4. คณะกรรมการฝ่ายรับ - จ่ายข้อสอบ ประกอบด้วย 4.1 นายสราญ คําอ้าย ประธานกรรมการ 4.2 นายธีรวัฒน์ บุญทวี กรรมการ 4.3 นักศึกษาฝึกประสบการณ์วิชาชีพครูประจําอาคาร กรรมการ 4.4 นายมนู กันทะวงค์ กรรมการและเลขานุการ หน้าที่ รับ - จ่ายข้อสอบ ตามอาคารและเวลาดังต่อไปนี้ ภาคเช้า - เวลา 07.45 น. รับข้อสอบจากกองกลางห้องศูนย์สอบ (อาคาร 2) เพื่อนําไปส่งกองกลาง ประจําอาคาร - เวลา 11.45 น. รับข้อสอบที่สอบแล้วจากกรรมการกลางประจําอาคาร เพื่อนําไปส่งกองกลางห้องศูนย์สอบ (อาคาร 2) ภาคบ่าย - เวลา 12.00 น. รับข้อสอบจากกองกลางห้องศูนย์สอบ (อาคาร 2) เพื่อนําไปส่งกองกลาง ประจําอาคาร เวลา 15.45 น. รับข้อสอบที่สอบแล้วจากกรรมการกลางประจําอาคาร เพื่อนําไปส่ง กองกลางห้องศูนย์สอบ (อาคาร 2) หมายเหตุ อุปกรณ์การสอบรับจากห้องศูนย์สอบวันแรก และส่งคืนวันสุดท้ายของการสอบ 4. คณะกรรมการกลางประจําศูนย์สอบ 4.1 อาคาร 2 (เรือนวิเชียร) กองกลางสนามสอบ สํานักงานอยู่ที่ห้องศูนย์สอบ อาคาร 2 ประกอบด้วย 4.1.1 นายสราญ คําอ้าย ประธานกรรมการ 4.1.2 นายมนู กันทะวงค์ กรรมการ 4.1.3 นายธีรวัฒน์ บุญทวี กรรมการ"),
        ("05_re.jpg","4.1.4 นางขนิษฐา คมขํา กรรมการ 4.1.5 นายพัทธยากร บุสสยา กรรมการ 4.1.6 นักศึกษาฝึกประสบการณ์วิชาชีพครูประจําอาคาร กรรมการ 4.1.7 นางบุปผา ธนะชัยขันธ์ กรรมการและเลขานุการ หน้าที่ 1. จัดอุปกรณ์ต่าง ๆ เกี่ยวกับการสอบ สําหรับจ่ายให้กรรมการกลางประจําอาคาร 2. เก็บรักษาข้อสอบทุกวิชาและจ่ายให้กรรมการกลางประจําอาคารเป็นรายวันเพื่อนําไปจัดสอบ ในแต่ละอาคาร 3. เก็บรักษากระดาษคําตอบทุกรายวิชาที่สอบเสร็จแล้วจากการนําส่งของกรรมการกลางประจํา อาคารในแต่ละวัน 4. ให้ครูประจําวิชารับกระดาษคําตอบที่สอบเสร็จเพื่อนําไปตรวจให้คะแนน โดย - วิชาที่สอบภาคเช้ารับ ในช่วงเวลา 13.30 - 16.00 น. - วิชาที่สอบภาคบ่ายรับ ในช่วงเวลา 08.30 - 12.00 น. ของวันถัดไป เว้นวันหยุดราชการ 5. รับและรวบรวมอุปกรณ์ต่าง ๆ เกี่ยวกับการสอบคืนจากกรรมการกลางประจําอาคาร 6. ประสานงานกับกรรมการกลางประจําอาคารในการแก้ไขปัญหาต่าง ๆ เกี่ยวกับการสอบ 7. ควบคุมการปฏิบัติงานของนักศึกษาฝึกประสบการณ์ในการรับ - ส่งข้อสอบไปยังอาคารต่าง ๆ 8. งานอื่น ๆ ตามที่ได้รับมอบหมาย 4.2 กรรมการกลางประจําอาคาร 4.2.1 อาคาร 3 (อาคารเรือนรัตน) สํานักงานอยู่ที่ชั้น 2 ห้องปฏิบัติการ 324 (วิทยาศาสตร์ ม.1) คณะกรรมการ ประกอบด้วย 4.2.1.1 นางสาววราภรณ์ เป้ามณี 4.2.1.2 นางนิตยา ศรีสุวรรณ์ 4.2.1.3 นักศึกษาฝึกประสบการณ์ประจําอาคาร 4.2.2 อาคาร 5 (อาคารเรือนวชิระ) สํานักงานอยู่ที่ชั้น 2 ห้องทะเบียนวัดผล คณะกรรมการ ประกอบด้วย 4.2.2.1 นางสาวอัญภัทร บุตรพรหม 4.2.2.2 นางสาวกัญปภัสร์ คําป้อ 4.2.2.3 นักศึกษาฝึกประสบการณ์ประจําอาคาร 4.2.3 อาคาร 7 (เรือนรัตนมณี) สํานักงานอยู่ที่ชั้น 2 ห้องศูนย์การเรียนรู้สังคมศึกษา คณะกรรมการ ประกอบด้วย 4.2.3.1 นายทวี ฤทธิเดช 4.2.3.2 นายกิตติพงศ์ ยอดชุมภู 4.2.3.3 นักศึกษาฝึกประสบการณ์ประจําอาคาร"),
        ("06_re.jpg","4.2.4 อาคาร 8 (เรือนศรีมรกต) สํานักงานอยู่ที่ชั้น 2 ห้องศูนย์การเรียนรู้ภาษาไทย คณะกรรมการ ประกอบด้วย 4.2.4.1 นางกิ่งดาว จองบุ๊ก 4.2.4.2 นางสาวมัณฑลี จิตเจนสุวรรณ 4.2.4.3 นักศึกษาฝึกประสบการณ์ประจําอาคาร 4.2.5 อาคาร 10 (อาคารเพชรรัตน์) สํานักงานอยู่ที่ชั้น 2 ห้องคอมพิวเตอร์ (1023) คณะกรรมการ ประกอบด้วย 4.2.5.1 นายปณวรรต บุญตาศานย์ 4.2.5.2 นางสาวหทัยรัตน์ ศรีวิโรจน์ 4.2.5.3 นักศึกษาฝึกประสบการณ์ประจําอาคาร 4.2.6 อาคาร 12 (อาคารวชิรดารา) สํานักงานอยู่ที่ชั้น 3 ห้องศูนย์การเรียนรู้คณิตศาสตร์ (1231) คณะกรรมการ ประกอบด้วย 4.2.6.1 นางจารุวรรณ ศรีจันทร์ 4.2.6.2 นาง ณ ชนก ปาลี 4.2.6.3 นางสาวสุภาสินี เสวันตุ่น 4.2.6.4 นักศึกษาฝึกประสบการณ์ประจําอาคาร หน้าที่ 1. วางแผนจัดการดําเนินการสอบในอาคารให้เป็นไปด้วยความเรียบร้อยตามระเบียบการสอบของ ทางราชการ 2. จัดระบบการรับ - ส่งข้อสอบทุกรายวิชาของแต่ละวันเพื่อนําไปดําเนินการสอบให้เป็นไปตามตารางสอบ 3. ภายหลังการสอบเสร็จในแต่ละวันให้นําข้อสอบและกระดาษคําตอบส่งคืนกรรมการกลางโดยส่งวันละ 2 ครั้ง คือ ภาคเช้าและภาคบ่าย โดยมีนักศึกษาฝึกประสบการณ์ประจําอาคารเป็นผู้ดําเนินการ 4. สรุปบัญชีรับ - ส่งข้อสอบ และกระดาษคําตอบภายในอาคารที่รับผิดชอบ ส่งคืนพร้อมข้อสอบ) 5. ประสานงานกับรองผู้อํานวยการฝ่ายจัดการศึกษาและกรรมการกลางเพื่อแก้ไขปัญหาต่าง ๆ เกี่ยวกับการสอบ 6. วันสุดท้ายของการสอบ ให้รวบรวมอุปกรณ์การสอบทุกชนิดส่งคืนกรรมการกลาง 7. ควบคุมดูแลการปฏิบัติงานของนักศึกษาฝึกประสบการณ์ประจําอาคาร 8. งานอื่น ๆ ตามที่ได้รับมอบหมาย"),
    ]

    for t in listfile:
        img  = Image.open('doc/{}'.format(t[0]),)
        result = pytesseract.image_to_string(img, lang='sarabun1', config='--psm 11')
        
        #eocr = ''.join(result)

        char = '\n'
        char2  = '\n\n'
       
        word = syllable_tokenize(result)

        word = [wo.replace(char, '') for wo in word]
        word = [wo2.replace(char2, '') for wo2 in word]

        tocr = ''.join(word)

        tocr.replace(' ', '')
       

        print(tocr)
      
        correct_text = t[1]
        ocr = len(tocr)
        text = len(correct_text)
        print("Correct text have a str = ",text,"| OCR text have a str = ",ocr)
        answer_list = []
        easy_list = []
        
        
        answer_list.append(correct_text) 
        easy_list.append(tocr)

    
        answer_array = np.array(answer_list)
        easy_array = np.array(easy_list)


        # store wrong cases and answer in dataframe
        df_easy_wrong = pd.DataFrame({'tesseract_wrong': easy_array[easy_array!=answer_array], 'answer': answer_array[easy_array!=answer_array]})


        df_easy_wrong_diff = compare_diff(df_easy_wrong, 'tesseract_wrong', 'answer')

        
        file = 'tesseract_ocr_report_{}.csv'.format(t[0])
        df_easy_wrong_diff.to_csv(file, encoding='utf-8-sig')
    