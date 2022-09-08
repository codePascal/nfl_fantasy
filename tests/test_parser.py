import unittest

import src.utils.parser as parser


class TestParser(unittest.TestCase):
    def test_get_request(self):
        result = parser.get_request("https://motherfuckingwebsite.com/")
        self.assertEqual("<!DOCTYPE html>", result.text[:15])

    def test_get_soup(self):
        result = parser.get_request("https://www.w3schools.com/html/html_tables.asp")
        soup = parser.get_soup(result)
        result = soup.find("title")
        self.assertEqual("HTML Tables", result.get_text(strip=True))

    def test_get_content(self):
        result = parser.get_request("https://www.w3schools.com/html/html_tables.asp")
        soup = parser.get_soup(result)
        content = parser.get_content(soup, "table")
        self.assertEqual(2, len(content))

    def test_get_data(self):
        result = parser.get_request("https://www.w3schools.com/html/html_tables.asp")
        soup = parser.get_soup(result)
        content = parser.get_content(soup, "table")
        data = parser.get_data(content[0])
        self.assertListEqual(['Company', 'Contact', 'Country'], data[0])
        self.assertListEqual(['Alfreds Futterkiste', 'Maria Anders', 'Germany'], data[1])
        self.assertListEqual(['Centro comercial Moctezuma', 'Francisco Chang', 'Mexico'], data[2])
        self.assertListEqual(['Ernst Handel', 'Roland Mendel', 'Austria'], data[3])
        self.assertListEqual(['Island Trading', 'Helen Bennett', 'UK'], data[4])
        self.assertListEqual(['Laughing Bacchus Winecellars', 'Yoshi Tannamuri', 'Canada'], data[5])
        self.assertListEqual(['Magazzini Alimentari Riuniti', 'Giovanni Rovelli', 'Italy'], data[6])
