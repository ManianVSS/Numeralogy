/*
 * Created by SharpDevelop.
 * User: Manian
 * Date: 25-Feb-17
 * Time: 7:03 PM
 * 
 * To change this template use Tools | Options | Coding | Edit Standard Headers.
 */
namespace Numeralogy
{
	partial class MainForm
	{
		/// <summary>
		/// Designer variable used to keep track of non-visual components.
		/// </summary>
		private System.ComponentModel.IContainer components = null;
		private System.Windows.Forms.TextBox NameTextBox;
		private System.Windows.Forms.TextBox TotalTextBox;
		private System.Windows.Forms.TextBox TermTotalTextBox;
		private System.Windows.Forms.Label label1;
		private System.Windows.Forms.Label label2;
		private System.Windows.Forms.Label label3;
		private System.Windows.Forms.NumericUpDown DesiredNumberNumericUpDown;
		private System.Windows.Forms.Label label4;
		private System.Windows.Forms.Button ExportNamesToFileButton;
		private System.Windows.Forms.SaveFileDialog ExportNameFileDialog;
		private System.Windows.Forms.Label label5;
		private System.Windows.Forms.NumericUpDown NameMaxLengthNumericUpDown;
		private System.Windows.Forms.TextBox GeneratedNameTextBox;
		
		/// <summary>
		/// Disposes resources used by the form.
		/// </summary>
		/// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
		protected override void Dispose(bool disposing)
		{
			if (disposing) {
				if (components != null) {
					components.Dispose();
				}
			}
			base.Dispose(disposing);
		}
		
		/// <summary>
		/// This method is required for Windows Forms designer support.
		/// Do not change the method contents inside the source code editor. The Forms designer might
		/// not be able to load this method if it was changed manually.
		/// </summary>
		private void InitializeComponent()
		{
			this.NameTextBox = new System.Windows.Forms.TextBox();
			this.TotalTextBox = new System.Windows.Forms.TextBox();
			this.TermTotalTextBox = new System.Windows.Forms.TextBox();
			this.label1 = new System.Windows.Forms.Label();
			this.label2 = new System.Windows.Forms.Label();
			this.label3 = new System.Windows.Forms.Label();
			this.DesiredNumberNumericUpDown = new System.Windows.Forms.NumericUpDown();
			this.label4 = new System.Windows.Forms.Label();
			this.ExportNamesToFileButton = new System.Windows.Forms.Button();
			this.ExportNameFileDialog = new System.Windows.Forms.SaveFileDialog();
			this.label5 = new System.Windows.Forms.Label();
			this.NameMaxLengthNumericUpDown = new System.Windows.Forms.NumericUpDown();
			this.GeneratedNameTextBox = new System.Windows.Forms.TextBox();
			((System.ComponentModel.ISupportInitialize)(this.DesiredNumberNumericUpDown)).BeginInit();
			((System.ComponentModel.ISupportInitialize)(this.NameMaxLengthNumericUpDown)).BeginInit();
			this.SuspendLayout();
			// 
			// NameTextBox
			// 
			this.NameTextBox.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
			this.NameTextBox.Location = new System.Drawing.Point(224, 41);
			this.NameTextBox.Margin = new System.Windows.Forms.Padding(4);
			this.NameTextBox.Name = "NameTextBox";
			this.NameTextBox.Size = new System.Drawing.Size(494, 22);
			this.NameTextBox.TabIndex = 0;
			this.NameTextBox.TextChanged += new System.EventHandler(this.NameTextBoxTextChanged);
			// 
			// TotalTextBox
			// 
			this.TotalTextBox.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
			this.TotalTextBox.Location = new System.Drawing.Point(585, 95);
			this.TotalTextBox.Margin = new System.Windows.Forms.Padding(4);
			this.TotalTextBox.Name = "TotalTextBox";
			this.TotalTextBox.ReadOnly = true;
			this.TotalTextBox.Size = new System.Drawing.Size(132, 22);
			this.TotalTextBox.TabIndex = 1;
			// 
			// TermTotalTextBox
			// 
			this.TermTotalTextBox.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
			this.TermTotalTextBox.Location = new System.Drawing.Point(585, 151);
			this.TermTotalTextBox.Margin = new System.Windows.Forms.Padding(4);
			this.TermTotalTextBox.Name = "TermTotalTextBox";
			this.TermTotalTextBox.ReadOnly = true;
			this.TermTotalTextBox.Size = new System.Drawing.Size(132, 22);
			this.TermTotalTextBox.TabIndex = 2;
			// 
			// label1
			// 
			this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
			this.label1.Location = new System.Drawing.Point(16, 41);
			this.label1.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
			this.label1.Name = "label1";
			this.label1.Size = new System.Drawing.Size(154, 50);
			this.label1.TabIndex = 3;
			this.label1.Text = "Registration Name: \r\nName Prefix For Export:";
			// 
			// label2
			// 
			this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
			this.label2.Location = new System.Drawing.Point(492, 95);
			this.label2.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
			this.label2.Name = "label2";
			this.label2.Size = new System.Drawing.Size(85, 28);
			this.label2.TabIndex = 4;
			this.label2.Text = "Name Sum:";
			// 
			// label3
			// 
			this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
			this.label3.Location = new System.Drawing.Point(433, 151);
			this.label3.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
			this.label3.Name = "label3";
			this.label3.Size = new System.Drawing.Size(144, 28);
			this.label3.TabIndex = 5;
			this.label3.Text = "Name Recursive Sum:";
			// 
			// DesiredNumberNumericUpDown
			// 
			this.DesiredNumberNumericUpDown.Location = new System.Drawing.Point(224, 219);
			this.DesiredNumberNumericUpDown.Margin = new System.Windows.Forms.Padding(4);
			this.DesiredNumberNumericUpDown.Name = "DesiredNumberNumericUpDown";
			this.DesiredNumberNumericUpDown.Size = new System.Drawing.Size(88, 22);
			this.DesiredNumberNumericUpDown.TabIndex = 6;
			// 
			// label4
			// 
			this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
			this.label4.Location = new System.Drawing.Point(28, 219);
			this.label4.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
			this.label4.Name = "label4";
			this.label4.Size = new System.Drawing.Size(169, 28);
			this.label4.TabIndex = 7;
			this.label4.Text = "Desired Number:";
			// 
			// ExportNamesToFileButton
			// 
			this.ExportNamesToFileButton.Location = new System.Drawing.Point(332, 219);
			this.ExportNamesToFileButton.Margin = new System.Windows.Forms.Padding(4);
			this.ExportNamesToFileButton.Name = "ExportNamesToFileButton";
			this.ExportNamesToFileButton.Size = new System.Drawing.Size(109, 28);
			this.ExportNamesToFileButton.TabIndex = 8;
			this.ExportNamesToFileButton.Text = "Export Names";
			this.ExportNamesToFileButton.UseVisualStyleBackColor = true;
			this.ExportNamesToFileButton.Click += new System.EventHandler(this.ExportNamesToFileButtonClick);
			// 
			// label5
			// 
			this.label5.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
			this.label5.Location = new System.Drawing.Point(28, 247);
			this.label5.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
			this.label5.Name = "label5";
			this.label5.Size = new System.Drawing.Size(169, 28);
			this.label5.TabIndex = 10;
			this.label5.Text = "Max Length:";
			// 
			// NameMaxLengthNumericUpDown
			// 
			this.NameMaxLengthNumericUpDown.Location = new System.Drawing.Point(224, 247);
			this.NameMaxLengthNumericUpDown.Margin = new System.Windows.Forms.Padding(4);
			this.NameMaxLengthNumericUpDown.Name = "NameMaxLengthNumericUpDown";
			this.NameMaxLengthNumericUpDown.Size = new System.Drawing.Size(88, 22);
			this.NameMaxLengthNumericUpDown.TabIndex = 9;
			// 
			// GeneratedNameTextBox
			// 
			this.GeneratedNameTextBox.Location = new System.Drawing.Point(448, 222);
			this.GeneratedNameTextBox.Name = "GeneratedNameTextBox";
			this.GeneratedNameTextBox.ReadOnly = true;
			this.GeneratedNameTextBox.Size = new System.Drawing.Size(243, 22);
			this.GeneratedNameTextBox.TabIndex = 11;
			// 
			// MainForm
			// 
			this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
			this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			this.ClientSize = new System.Drawing.Size(752, 286);
			this.Controls.Add(this.GeneratedNameTextBox);
			this.Controls.Add(this.label5);
			this.Controls.Add(this.NameMaxLengthNumericUpDown);
			this.Controls.Add(this.ExportNamesToFileButton);
			this.Controls.Add(this.label4);
			this.Controls.Add(this.DesiredNumberNumericUpDown);
			this.Controls.Add(this.label3);
			this.Controls.Add(this.label2);
			this.Controls.Add(this.label1);
			this.Controls.Add(this.TermTotalTextBox);
			this.Controls.Add(this.TotalTextBox);
			this.Controls.Add(this.NameTextBox);
			this.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
			this.Margin = new System.Windows.Forms.Padding(4);
			this.Name = "MainForm";
			this.Text = "Numeralogy";
			((System.ComponentModel.ISupportInitialize)(this.DesiredNumberNumericUpDown)).EndInit();
			((System.ComponentModel.ISupportInitialize)(this.NameMaxLengthNumericUpDown)).EndInit();
			this.ResumeLayout(false);
			this.PerformLayout();

		}
	}
}
