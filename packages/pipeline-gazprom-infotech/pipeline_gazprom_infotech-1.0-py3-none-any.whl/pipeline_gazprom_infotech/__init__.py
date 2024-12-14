"""Base Infotech XML stuff."""
from lxml import etree as ET


def it_date(dtime):
    """Return string date in Infotech format for given datetime value."""
    return "{:02d}.{:02d}.{}".format(dtime.day, dtime.month, dtime.year)


class InfotechError(Exception):
    """Infotech exceptions."""


class Typeobj:
    """Attributes of the TYPEOBJS Infotech XML section."""

    Section = 'TYPEOBJS'
    Title = 'TYPEOBJ'

    Id = 'IDTYPEOBJ'
    Name = 'TITLE'


class InfotechBase:
    """Abstract base Infotech XML class."""

    root = None
    typobjs = None

    def save(self, file_name, encoding="windows-1251"):
        """Save XML string to file.

        Python >= 3.8
        https://stackoverflow.com/questions/62163221/creating-xml-file-with-a-specific-order-or-attributes-using-python
        """
        with open(file_name, 'wb') as out:
            out.write(ET.tostring(self.root, xml_declaration=True, encoding=encoding, pretty_print=True))

    def add_types(self, it_dict):
        """Add given dict to TYPEOBJS."""
        for code, name in it_dict.items():
            ET.SubElement(self.typobjs, Typeobj.Title, {
              Typeobj.Id: code,
              Typeobj.Name: name,
            })
