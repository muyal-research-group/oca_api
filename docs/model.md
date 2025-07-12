<p align="justify">
    The <b>QLX Model</b> is a multi-dimensional to organize and query complex items through a set of fundamental entities: <b>Xvars</b> (attributes), <b>Catalogs</b> (collections of attributes), <b>Observatories</b> (scoped spaces for querying), and <b>Products</b> (primary entities with specific characteristics). The QLX Model allows for flexible, dynamic querying by structuring data around Xvars across various dimensions, such as spatial, temporal, interest, observable metrics, informational data, and product types.
</p>

Below, we define each component of the QLX Model mathematically and describe how they connect to enable powerful, context-based querying.

## Mathematical Model Definitions


### 1. Xvar (Xvariable)
An <b>Xvar</b> (short for Xvariable) is a fundamental attribute or characteristic that defines properties across different dimensions. Each Xvar is represented as a tuple containing essential fields:

Let:

- $X$ be the set of all possible Xvars.

- An Xvar \( X_{vi} \) is defined as:

$$
Xv_{i} = (\text{xvid}, \text{type}, \text{value}, \text{xtype}, \text{parentid}, \text{order})
$$

where:

- **\( \text{xvid} \)**: Unique identifier for the Xvar.

- **\( \text{type} \)**: The label or category that describes the Xvar (e.g., "Country," "Date").

- **\( \text{value} \)**: The data or value associated with the Xvar (e.g., "MX" for Country).

- **\( \text{xtype} \)**: The classification type, representing one of the following dimensions:

    - **SPATIAL (S)**: Location-based attributes.

    - **TEMPORAL (T)**: Time-related attributes.

    - **INTEREST (I)**: Demographic or categorical variables.

    - **OBSERVABLE (O)**: Measurable metrics.

    - **INFO (F)**: Metadata or additional information.

    - **PRODUCTTYPE (P)**: Specifies the type of product.

- **\( \text{parentid} \)**: Identifier of the parent Xvar, if it exists in a hierarchy (e.g., State with Country as a parent).

- **\( \text{order} \)**: Hierarchical level within the classification; -1 indicates no hierarchy.

Each Xvar can therefore be identified as an attribute that can define, describe, or classify a product within one or more dimensions.


### 2. Catalogs

**Catalogs** in the QLX Model are collections of Xvars organized by specific dimensions. Catalogs allow Xvars to be grouped under common categories and validated within the context of an observatory.

Let:

- \( C \) be the set of all catalogs in the QLX Model.

- \( C_{\text{dimension}} \subset X \) represents the set of Xvars in a catalog for a specific dimension.

- A **Catalog** \( C_d \) is a set of Xvars for a given dimension \( d \) (e.g., spatial, temporal).

For each catalog dimension, we define:

$$
C_d = \{ X_{vi} \in X \mid X_{vi} \text{ matches the dimension type } d \}
$$

where **dimension types** include:

- **\( C_{\text{spatial}} \)**: Catalog of spatial Xvars (e.g., country, state).

- **\( C_{\text{temporal}} \)**: Catalog of temporal Xvars (e.g., year, date).

- **\( C_{\text{interest}} \)**: Catalog of demographic or categorical Xvars (e.g., age group, sex).

- **\( C_{\text{observable}} \)**: Catalog of measurable variables (e.g., mortality rate).

- **\( C_{\text{info}} \)**: Catalog of informational or metadata Xvars (e.g., data source).

- **\( C_{\text{producttype}} \)**: Catalog of product type Xvars (e.g., map, report).

By organizing Xvars into catalogs, the QLX Model supports standardized filtering and dynamic extension of attributes.

### 3. Observatory

An **Observatory** in the QLX Model is a defined scope or context where users can query products based on a specific set of catalog constraints. It restricts queries to a predefined subset of Xvars, allowing for structured and context-specific data exploration.

Let:

- **\( O \)** be the set of all observatories.

- Each **Observatory** \( O_i \) is defined as:

$$
O_i = (\text{oid}, \mathcal{P}_{O_i}, C_{O_i})
$$

where:

- **oid**: A unique identifier for the observatory.

- **\( \mathcal{P}_{O_i} \subset \mathcal{P} \)**: The set of products within this observatory.

- **\( C_{O_i} = (C_{\text{spatial}}, C_{\text{temporal}}, C_{\text{interest}}, C_{\text{observable}}, C_{\text{info}}, C_{\text{producttype}}) \)**: A set of catalogs that specify the allowed Xvars in each dimension.

For an observatory to accept a query, it must match the constraints of its defined catalogs. This scoped environment enables focused data retrieval within a given context (e.g., a health observatory limited to specific countries and demographic attributes).


### 4. Products

A **Product** is the main entity of interest within the QLX Model, representing items or phenomena described by a specific set of Xvars across various dimensions. Each product is a unique combination of Xvar values and is identified by its product ID.

Let:

- \( \mathcal{P} \) be the set of all products in the system.

- Each product \( p_i \in \mathcal{P} \) is defined by:

$$
p_i = (\text{pid}, X_{i})
$$

where:

- **pid**: A unique identifier for the product.

- **\( X_i \subset X \)**: A subset of Xvars describing the product’s attributes across dimensions, including spatial, temporal, interest, observable, info, and product type.

Each product is therefore represented as a unique combination of Xvars, allowing for flexible, multi-dimensional filtering based on attributes defined in the catalogs.

## Querying in the QLX Model

In the QLX Model, queries are executed within observatories based on combinations of Xvars from the observatory’s allowed catalogs. Each query is checked against the observatory’s catalog constraints, and only products that match the specified Xvars across dimensions are returned.

Let:

- $Q$ represent a query.

- **\( X_Q \subset X \)** represent the set of Xvars specified in the query.

- The query \( Q \) is valid within an observatory \( O_i \) if:

$$
X_Q \subseteq C_{\text{spatial}} \cup C_{\text{temporal}} \cup C_{\text{interest}} \cup C_{\text{observable}} \cup C_{\text{info}} \cup C_{\text{producttype}}
$$

where each subset is taken from \( C_{O_i} \), the observatory’s defined catalogs.

### Result Set

The result set of a query is the subset of products \( p_i \in \mathcal{P}_{O_i} \) that match all specified Xvars in \( X_Q \).

### Example of a Query

Given an observatory \( O_1 \) with the following catalogs:

- **\( C_{\text{spatial}} \)**: \{ "Country(MX)", "State(SLP)" \}

- **\( C_{\text{temporal}} \)**: \{ "Date(2020)" \}

- **\( C_{\text{interest}} \)**: \{ "Age(18-65)" \}

- **\( C_{\text{observable}} \)**: \{ "Mortality.RawRatio" \}

- **\( C_{\text{producttype}} \)**: \{ "Report" \}

A valid query within \( O_1 \) might look like:

$$
Q = \{ \text{Country(MX)}, \text{State(SLP)}, \text{Date(2020)}, \text{Age(18-65)}, \text{Mortality.RawRatio}, \text{Report} \}
$$

This query would retrieve products that meet all specified criteria within the scope of \( O_1 \), filtering based on the observatory’s defined Xvar catalogs.
