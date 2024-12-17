import re
import periodictable as pt

##############################################
# CUSTOM ELEMENT TO HANDLE CODES OUT OF RANGE
##############################################

class CounterElement(pt.core.Element):
    """
    A custom element class to handle elements with codes out of the periodic table range.\n
    It store in the mass (`900 + <loop counter>`) how many time we looped out of range over the periodic table to finaly fit the ASCII code in the table.\n
    The name store the element that we finally are able to fit into as last part this element name.\n
    """

    def __init__(self, cnt: int, el: pt.core.Element):
        """Create a CounterElement\n

        Args:
            cnt (int): the loop counter (i.e how many time we looped out of range over the periodic table)
            el (pt.core.Element): the element that we finally are able to fit into
        """

        # Initialize the parent class
        super().__init__(
            name=f"Counterium-{el.name}-{cnt}",
            symbol=f"Ct{el.symbol}{cnt}",
            Z=900 + cnt,
            ions=(),
            table="public"
        )
        
        self._mass = 900 + cnt

    @property
    def mass(self):
        return self._mass



    @mass.setter
    def mass(self, value):
        self._mass = value
    

    
    @classmethod
    def split_symbol(cls, symbol: str) -> tuple[str, int]:
        """Split a symbol into the element symbol and the counter

        Args:
            symbol (str): the symbol to split

        Returns:
            tuple[str, int]: return the element symbol and the counter
        """        """
        
        """
        symbol = symbol[2:] # remove the "Ct" at the beginning
        
        elsy = ''.join(filter(str.isalpha, symbol)) # get the element name
        cnt = ''.join(filter(str.isdigit, symbol)) # get the counter

        return elsy, int(cnt)

##############################################
# GET ELEMENTS
##############################################

def get_el_by_number(number: int) -> pt.core.Element:
    """Return the element by its number

    Args:
        number (int): the number of the element

    Returns:
        pt.core.Element: the element
    """
    return pt.elements[number]



def get_el_by_name(name: str) -> pt.core.Element:
    """Return the element by its name

    Args:
        name (str): the name of the element

    Returns:
        pt.core.Element: the element
    """    

    return pt.elements.name(name)



def get_el_by_symbol(symbol: str) -> pt.core.Element:
    """Return the element by its symbol

    Args:
        symbol (str): the symbol of the element

    Returns:
        pt.core.Element: the element
    """
    if re.match(r'Ct([A-Z][a-z]?\d*)', symbol): # if its a CounterElement
        
        sym, cnt = CounterElement.split_symbol(symbol)

        return CounterElement(int(cnt),pt.elements.symbol(sym))
    
    return pt.elements.symbol(symbol)



def get_last_el() -> pt.core.Element:
    """Return the last element of the periodic table

    Returns:
        pt.core.Element: the last element
    """    
    bst = 0
    for e in pt.elements:
        if e.number > bst:
            bst = e.number
    return get_el_by_number(bst)

##############################################
# TEXT ----> ELEMENTS
##############################################

def turn_chr_into_el(character: chr) -> pt.core.Element:
    """Convert a character into an element

    Args:
        character (chr): the character to convert

    Returns:
        pt.core.Element: the resulting element
    """    
    el = None
    last = get_last_el().number

    code = ord(character)

    #gotta truncate or it won't fit periodic table
    if code > last:
        quot = code // last
        truncated_code = code % last

        return CounterElement(
            quot,
            get_el_by_number(truncated_code)
        )

    else:
        return get_el_by_number(code)



def turn_str_into_el(string: str) -> list[pt.core.Element]:
    """Convert a string into a list of elements

    Args:
        string (str): the string to convert

    Returns:
        list[pt.core.Element]: the resulting list of elements
    """    
    lst: list[pt.core.Element] = []
    for c in string:
        lst.append(turn_chr_into_el(c))
    return lst

##############################################
# ELEMENTS ----> TEXT
##############################################

def turn_el_into_chr(element: pt.core.Element) -> chr:
    """Convert an element into a character

    Args:
        element (pt.core.Element): the element to convert

    Returns:
        chr: the resulting character
    """    
    if (element.number < 900):
        #its a normal element
        return chr(element.number)
    else:
        #its a loop counter element        
        sym, cnt = CounterElement.split_symbol(element.symbol)

        excess = cnt * get_last_el().number

        return chr(excess + get_el_by_symbol(sym).number)



def turn_el_into_str(element_list: list[pt.core.Element]) -> str:
    """Convert a list of elements into a string

    Args:
        element_list (list[pt.core.Element]): the list of elements to convert

    Returns:
        str: the resulting string
    """    
    string = ""
    for e in element_list:
        string += turn_el_into_chr(e)
    return string

# Code by NilsMT on GitHub