// По мере осознания можно убивать избыточные комменты, чтобы не опухнуть.

// Сейчас этот пример выводит в аутпут считываемый файл в формате Имя ячейки - Содержимое ячейки.
// A1 - бла-бла
// B1 - dfdfdf
// A2 - flgkg
// B2 - hkhkh
// Это зачаток реализации парсинга файлов xlsx путем применения SAX-парсера XML.
// Да-да XML, котоый сидит внутри архива с расширением xlsx.
// Такие дела.
// Ибо SAX-парсер быстр и жрет мало памяти.
// Поэтому постараемся сразу заточиться под конские объемы заранее.

// Там где меня хватило постарался объяснить как понимаю.
// Где нет - скопипастил из оф.доки Апача и других.

// Объявляем наш пакет работы с xlsx.
// Да, не с xls, а именно с xlsx.
// Их можно объединить генериками, но пока это сложна для моего уровня.
package com.LoadFromXLSX;

import org.apache.poi.openxml4j.opc.OPCPackage;
import org.apache.poi.util.XMLHelper;
import org.apache.poi.xssf.eventusermodel.XSSFReader;
import org.apache.poi.xssf.model.SharedStringsTable;
import org.xml.sax.*;
import org.xml.sax.helpers.DefaultHandler;

import javax.xml.parsers.ParserConfigurationException;
import java.io.InputStream;

// Главный и единственный класс программы парсинга.
// Должен совпадать с именем файла, в котором объявлен.
// Main.java.
public class Main {

    // Метод main - входная точка при вызове.
    // Параметром идет массив строк.
    // В нем аргументы из командной строки.
    // Разделитель?
    // Дополнительно декларируется, что наш класс умеет кидать исключительную ситуацию.
    public static void main(String[] args) throws Exception {

        // Создадим экземпляр нашего класса и назовем громким именем)))
        Main xlsxParserProcessor = new Main();

        // Вызовем метод процессинга одного рабочего листа из файла.
        // args[0] - путь к файлу, переданный в командной строке.
        // xlsxParserProcessor.processOneSheet("C:\\w8.xlsx");

        // Тут я пытался сделать экзешник, в который передать путь в комадной строке.
        if (args.length != 0) {
            xlsxParserProcessor.processOneSheet(args[0]);
        }
    }

    // Метод процессинга одного рабочего листа из файла.
    public void processOneSheet(String filename) throws Exception {

        // OPCPackage - контейнер, который может содержать в себе несколько файлов.
        // Походу это спец штука для чтения xlsx, т.к. xlsx это по факту зип архив
        // С кучей файлов внутри.
        OPCPackage pkg = OPCPackage.open(filename);

        // Создаем экземпляр класса-читателя нашего "архива"
        // Позволяет получать доступ к файлам-частям внутри архива.
        // This class makes it easy to get at individual parts of an OOXML .xlsx file,
        // suitable for low memory sax parsing or similar.
        // It makes up the core part of the EventUserModel support for XSSF.
        XSSFReader r = new XSSFReader(pkg);

        // Короче это такая херня, которая оптимизирует открытие/чтение файла
        // Путем кэширования дохуа повторяющихся значений в файле.
        // Table of strings shared across all sheets in a workbook.
        // A workbook may contain thousands of cells containing string (non-numeric) data.
        // Furthermore this data is very likely to be repeated across many rows or columns.
        // The goal of implementing a single string table that is shared across the workbook
        // is to improve performance in opening and saving the file by only reading
        // and writing the repetitive information once.
        // Consider for example a workbook summarizing information for cities within various countries.
        // There may be a column for the name of the country, a column for the name of each city in that country,
        // and a column containing the data for each city. In this case the country name is repetitive,
        // being duplicated in many cells. In many cases the repetition is extensive,
        // and a tremendous savings is realized by making use of a shared string
        // table when saving the workbook. When displaying text in the spreadsheet,
        // the cell table will just contain an index into the string table as the value of a cell, instead of the full string.
        // The shared string table contains all the necessary information for displaying the string:
        // the text, formatting properties, and phonetic properties (for East Asian languages).
        SharedStringsTable sst = r.getSharedStringsTable();

        // А это уже читатель xml-кишок, которые сидят в архиве.
        XMLReader parser = fetchSheetParser(sst);

        // Короче - rId1 - это внутренее имя первого рабочего листа с рабочей книге.
        // Тут возможны дрова ибо если их несколько, то надо понимать, как с ними оперировать.
        // Типа откуда счет и вот это вот все.
        // Создается поток чтения (байтов?) нашего листа.
        // To look up the Sheet Name / Sheet Order / rID,
        //  you need to process the core Workbook stream.
        // Normally it's of the form rId# or rSheet#
        InputStream sheet2 = r.getSheet("rId1");

        // Какие-то мутки с потоком.
        // На его основе создается источник, который пользуется SAX-ом
        // А ещё в следующей строке сказано, что т.к. это а-ля опен-сорс, то никаких гарантий)))
        // This module, both source code and documentation, is in the Public Domain, and comes with NO WARRANTY.
        // The SAX parser will use the InputSource object to determine how to read XML input.
        InputSource sheetSource = new InputSource(sheet2);

        // А теперь парсер xml давай парсь наш источник.
        parser.parse(sheetSource);

        // Закрыть наш лист после того как отколбасили.
        sheet2.close();
    }

    // Ну короче - дай парсер, которым будем колбасить xml.
    // Сил уже нет)))
    // А, вон чо, парсер это класс, который композицией включен в наш главный класс Main
    // И этот метод возвращает нам экземпляр этого класса-обработчика.
    public XMLReader fetchSheetParser(SharedStringsTable sst) throws SAXException, ParserConfigurationException {
        XMLReader parser = XMLHelper.newXMLReader();
        ContentHandler handler = new Main.SheetHandler(sst);
        parser.setContentHandler(handler);
        return parser;
    }

    private static class SheetHandler extends DefaultHandler {

        private SharedStringsTable sst;
        private String lastContents;
        private boolean nextIsString;

        // Конструктор
        private SheetHandler(SharedStringsTable sst) {
            this.sst = sst;
        }

        // Метод-обработчик события - нихуясе, начался новый элемент.
        // Там внутри обрабтываются только элементы-ячейки, поэтому сравнивается с "c".
        // По этому событию отписывается имя ячейки, например A1.
        public void startElement(String uri, String localName, String name, Attributes attributes) throws SAXException {

            //System.out.println(name);
            // c => cell
            if(name.equals("c")) {
                // Print the cell reference
                System.out.print(attributes.getValue("r") + " - ");
                // Figure out if the value is an index in the SST
                String cellType = attributes.getValue("t");
                if(cellType != null && cellType.equals("s")) {
                    nextIsString = true;
                } else {
                    nextIsString = false;
                }
            }
            // Clear contents cache
            lastContents = "";
        }

        // Это обработчик события - ну ёпт, элемент кончился.
        // Там внутри v - это маркер содержимого ячейки.
        // По этому событию отписывается содержимое ячейки.
        // И какая-та инфа запоминается.
        public void endElement(String uri, String localName, String name) throws SAXException {

            // Process the last contents as required.
            // Do now, as characters() may be called more than once
            if(nextIsString) {
                int idx = Integer.parseInt(lastContents);
                lastContents = sst.getItemAt(idx).getString();
                nextIsString = false;
            }

            // v => contents of a cell
            // Output after we've seen the string contents
            if(name.equals("v")) {
                System.out.println(lastContents);
            }
        }

        // Это я не понял пока, собирает в одну строку что-то...
        // Может быть значение тэга.
        public void characters(char[] ch, int start, int length) {
            lastContents += new String(ch, start, length);
        }
    }
}