
import  ocaapi.querylang as qlx
import pytest

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_sv():
    xs = [
        """
        SV = Country(MX),State(Aguas),State(SLP)->City(Valles)
        """,
        """
        SV = Country(MX)->State(SLP)
        """,
        """
        SV = Country(MX)->State(SLP)->City(Valles), Country(MX)->State(TAMPS)
        """

    ]
    for x in xs:
        res = qlx.sv.parseString(x)
        print(f"X: {x}")
        print("_"*50)
        print(res)
        print("_"*50)

@pytest.mark.skip("")
@pytest.mark.asyncio
async def test_tv():
    xs = [
        """
        TV = Date(1,1,2020), Year(1997)
        """,
        """
        TV = Date(MAY,1,2020)
        """,
        """
        TV = [Date(1,1,2020), Date(1,1,2024)]
        """,
        """
        TV = Year(2000)
        """,
        """
        TV = [Year(2000), Year(2024)]
        """,
        """
        TV = Range(1997,2024,1)
        """,

    ]
    for x in xs:
        res = qlx.tv.parseString(x)
        print(f"X: {x}")
        print("_"*50)
        print(res)
        print("_"*50)



@pytest.mark.asyncio
async def test_iv():
    xs = [
        """
        IV = Sex(Male)
        """,
        """
        IV = Sex(Female,Male)
        """,
        """
        IV = Chapter(II)->Block(C50)->Code(4)->Modifier(1)
        """,
    ]

    for x in xs:
        res = qlx.iv.parseString(x)
        print(f"X: {x}")
        print("_"*50)
        print(res)
        print("_"*50)