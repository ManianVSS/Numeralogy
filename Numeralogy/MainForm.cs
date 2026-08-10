/*
 * Created by SharpDevelop.
 * User: Manian
 * Date: 25-Feb-17
 * Time: 7:03 PM
 * 
 * To change this template use Tools | Options | Coding | Edit Standard Headers.
 */
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;
using System.IO;

namespace Numeralogy
{
	/// <summary>
	/// Description of MainForm.
	/// </summary>
	public partial class MainForm : Form
	{
		private string exportFileName;
		private FileStream exportFileStream;
		
		private static Dictionary<char,int> charMap=new Dictionary<char,int>();
		
		private List<char> vowelArray= new List<char>(new char[]{'a','e','i','o','u'});
		
		private bool isVowel(char c)
		{
			return vowelArray.Contains(c);
		}
		
		private void InitDictionary()
		{
			charMap[' ']=0;
			charMap['\t']=0;
			charMap['\n']=0;
			charMap['a']=1;
			charMap['b']=2;
			charMap['c']=3;
			charMap['d']=4;
			charMap['e']=5;
			charMap['f']=8;
			charMap['g']=3;
			charMap['h']=5;
			charMap['i']=1;
			charMap['j']=1;
			charMap['k']=2;
			charMap['l']=3;
			charMap['m']=4;
			charMap['n']=5;
			charMap['o']=7;
			charMap['p']=8;
			charMap['q']=1;
			charMap['r']=2;
			charMap['s']=3;
			charMap['t']=4;
			charMap['u']=6;
			charMap['v']=6;
			charMap['w']=6;
			charMap['x']=5;
			charMap['y']=1;
			charMap['z']=7;
			charMap['A']=1;
			charMap['B']=2;
			charMap['C']=3;
			charMap['D']=4;
			charMap['E']=5;
			charMap['F']=8;
			charMap['G']=3;
			charMap['H']=5;
			charMap['I']=1;
			charMap['J']=1;
			charMap['K']=2;
			charMap['L']=3;
			charMap['M']=4;
			charMap['N']=5;
			charMap['O']=7;
			charMap['P']=8;
			charMap['Q']=1;
			charMap['R']=2;
			charMap['S']=3;
			charMap['T']=4;
			charMap['U']=6;
			charMap['V']=6;
			charMap['W']=6;
			charMap['X']=5;
			charMap['Y']=1;
			charMap['Z']=7;
			
		}
		
		private int FindSum(string name)
		{
			int sum=0;
			
			foreach(char c in name)
			{
				if(charMap.ContainsKey(c))
				{
					sum+=charMap[c];
				}
			}
			
			return sum;
		}
		
		private int DigitSum(int number)
		{
			string numberString=""+number;
			int sum=0;
			
			foreach(char digit in numberString)
			{
				sum+=(digit-'0');
			}
			return sum;
		}
		
		private int FindTermSum(int nameSum)
		{
			while(nameSum>9)
			{
				nameSum=DigitSum(nameSum);
			}
			return nameSum;
		}
		
		public MainForm()
		{
			InitializeComponent();
			InitDictionary();
		}
		
		void NameTextBoxTextChanged(object sender, EventArgs e)
		{
			int sum=FindSum(NameTextBox.Text);
			TotalTextBox.Text=""+sum;
			TermTotalTextBox.Text=""+FindTermSum(sum);
		}
		
		public delegate void NameFoundEventHandler(string name);
		
		void ExportNameTree(decimal maxlength,decimal desiredSum, NameFoundEventHandler nfeHandler, string treeParentNamePart="")
		{
			if(maxlength<=0)
			{
				return;
			}
			for(char iterChar='a'; iterChar<='z';iterChar++)
			{
				if(treeParentNamePart.EndsWith(""+iterChar))
				{
					continue;
				}
				
				if(isVowel(iterChar)&& isVowel(treeParentNamePart[treeParentNamePart.Length-1]))
				{
					continue;
				}
				
				string itername=treeParentNamePart+iterChar;
				//int cursum=FindSum();
				
				if(charMap[iterChar]>=desiredSum)
				{
					if(charMap[iterChar]==desiredSum)
					{
						nfeHandler(itername);
					}
					continue;
				}
				//else
				{
					ExportNameTree(maxlength-1,desiredSum-charMap[iterChar],nfeHandler,itername);
				}
			}
		}
		
		void WriteFoundNameToFile(string Name)
		{
			//GeneratedNameTextBox.Text=Name;		
			File.AppendAllText(exportFileName, "\r\n"+Name);
		}
		
		void ExportNamesToFileButtonClick(object sender, EventArgs e)
		{
			if((DesiredNumberNumericUpDown.Value>0)&&(NameMaxLengthNumericUpDown.Value>0))
			{
				switch(ExportNameFileDialog.ShowDialog())
				{
					case DialogResult.OK:
						exportFileName=ExportNameFileDialog.FileName;	
						File.WriteAllText(exportFileName,"Names for the combination Name Prefix: "+NameTextBox.Text+", Desired sum: "+DesiredNumberNumericUpDown.Value+" and Maximum Length: "+NameMaxLengthNumericUpDown.Value+" is as follows.");
						//exportFileStream=new FileStream(exportFileName,FileMode.CreateNew);
						int namePrefixSum=FindSum(NameTextBox.Text);
						ExportNameTree(NameMaxLengthNumericUpDown.Value-NameTextBox.Text.Length,DesiredNumberNumericUpDown.Value-namePrefixSum,WriteFoundNameToFile, NameTextBox.Text);
						break;
				}
			}
		}
		
//		bool isAllowedNameLetter(char c)
//		{
//			c=char.ToLower(c);
//			return ((c>='a')&&(c<='z')) || (c==' ') || (c=='.') || (c==(char)Keys.Back);
//		}
		
//		void NameTextBoxKeyDown(object sender, KeyEventArgs e)
//		{
//			//if(!isAllowedNameLetter((char) e.KeyValue))
//			{
//				//	e.SuppressKeyPress=true;
//			}
//		}
		
	}
}
