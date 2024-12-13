.. code-block:: shell
    $ rs # Generate a random string of lenth 10.
    8Vlp66h9Wc


.. code-block:: shell
    $ rs -l 16 # Generate a random string of lenth 16.
    xVOKhNEe0xJ607Ch


.. code-block:: shell
    $ rs -l 16 -c a # Specify a character set.
    ~_Ak-=0PNP}fo]j&h


.. code-block:: python
    length = 20
    rs = random_string(length)
    strength = strength(length, len(candidate))
    print(rs, strength) # khfT6pghUm1n1cpZhTar 119
    x = rs2int(rs)
    y = int2rs(x)
    print(rs, x, y) # khfT6pghUm1n1cpZhTar 415159970288189017488437341125226411 khfT6pghUm1n1cpZhTar