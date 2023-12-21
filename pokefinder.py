#! /usr/bin/env python3

import argparse
from InquirerPy import inquirer
import pokebase as pb

def reverse_mask(nums, start=1, end=1025):
    for num in nums:
        print(num)
    nums = sorted(nums)  # make sure your nums are in increasing order
    prev = start - 1
    result = []
    for num in nums:
        if prev + 1 != num: # check if there's a gap
            result.append((prev + 1, num - 1))
        prev = num
    # add the remaining end part
    if nums[-1] != end:
        result.append((nums[-1] + 1, end))
    
    return result

def main():
    #Set command line arguments 
    parser = argparse.ArgumentParser()
    poke_message="Please enter a comma separated list of poke species, name or number"
    region_message="Please enter a comma separated list of regions to filter by those forms"
    parser.add_argument('-p', help=poke_message)
    parser.add_argument('-r', help=region_message)
    parser.add_argument('-v', help="Verbose mode", action='store_true')

    args = parser.parse_args()

    #pokemon flag
    if args.p:
        poke_check = args.p
    else:
        poke_check = inquirer.text(message=f"{poke_message}:").execute()

    #region flag
    if args.r:
        regions = args.r
    else:
        regions = inquirer.text(message=f"{region_message}:").execute()

    poke_list = poke_check.split(",")

    numbers_to_reverse = []

    #print(dir(pb))

    print("Checking for spelling errors...")
    for poke in poke_list:
        if poke.isdigit() and int(poke) <= 1025:
            print(f"Found: #{poke}")
            numbers_to_reverse.append(int(poke))
        else:
            #query pokeapi for the name
            pokemon = pb.pokemon(poke)
            if pokemon.id_:
                print(f"Found: #{pokemon.id_} - {pokemon.name.title()}")
                numbers_to_reverse.append(pokemon.id_)
            else:
                print(f"Not Found: {poke}")


    #reverse the numbers
    final_list = reverse_mask(numbers_to_reverse)

    #print regions
    r = 1
    regions_list = regions.split(",")
    for region in regions_list:
        if r==len(regions_list):
            print(f"{region}&",end="")
        else:
            print(f"{region},",end="")
        r+=1

    p = 1
    for spread in final_list:
        if p==len(final_list):
            print(f"!{spread[0]}-{spread[1]}",end="")
        else:
            print(f"!{spread[0]}-{spread[1]}&",end="")
        p+=1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")