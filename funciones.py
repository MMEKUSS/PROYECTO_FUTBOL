{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "e4b9962f",
   "metadata": {},
   "source": [
    "ESTOS SERÁN LAS FUNCIONES QUE UTILICEMOS EN NUESTRO PROYECTO"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "5804e715",
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests\n",
    "from bs4 import BeautifulSoup\n",
    "\n",
    "def obtener_soup(url):\n",
    "    response = requests.get(url)\n",
    "    soup = BeautifulSoup(response.text, \"html.parser\")\n",
    "    \n",
    "    return soup"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "590bba75",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "base",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.14.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
