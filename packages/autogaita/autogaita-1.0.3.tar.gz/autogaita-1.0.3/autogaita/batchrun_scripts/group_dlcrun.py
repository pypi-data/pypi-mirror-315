import autogaita


def group_dlcrun():
    """
    Batchrun script to run AutoGaitA Group for Results obtained with AutoGaitA DLC.
    folderinfo & cfg dictionaries must be configured as explained in our documentation. See the "AutoGaitA without the GUI" section of our documentation for references to in-depth explanations to all dictionary keys (note that each key of dicts corresponds to some object in the AutoGaitA Group GUI)
    """
    # folderinfo
    # => Note that length of folderinfo's group_names & group_dirs lists determines how #    many groups are compared.
    # => Also note that indices must correspond (i.e., idx #    1's name will be used #    for dataset stored in group_dir's idx 1)
    folderinfo = {}
    folderinfo["group_names"] = [
        # ----------
        # RM Dataset
        # "5mm",
        # "12mm",
        # "25mm",
        # -------
        # Interaction Issue Dataset
        # "Control",
        # "Silenced",
        # --------
        # Testing Dataset
        # "one",
        # "two",
        # --------
        # Beam x Age for Manuscript
        "3m_5mm",
        "3m_12mm",
        "3m_25mm",
        "24m_5mm",
        "24m_12mm",
        "24m_25mm",
    ]
    folderinfo["group_dirs"] = [
        # --------------------------
        # Full Dataset (39 subjects)
        # "/Users/mahan/sciebo/Research/AutoGaitA/Mouse/Sanity Test Interaction Graziana/Result 10 joints/Control Full",
        # "/Users/mahan/sciebo/Research/AutoGaitA/Mouse/Sanity Test Interaction Graziana/Result 10 joints/Silenced Full/",
        # --------------------------
        # Reduced Dataset (5 subjects)
        # "/Users/mahan/sciebo/Research/AutoGaitA/Mouse/Sanity Test Interaction Graziana/Result 10 joints/Control",
        # "/Users/mahan/sciebo/Research/AutoGaitA/Mouse/Sanity Test Interaction Graziana/Result 10 joints/Silenced/",
        # --------------------------
        # Testing Dataset
        # "/Users/mahan/sciebo/Research/AutoGaitA/Mouse/Testing/Group 1/",
        # "/Users/mahan/sciebo/Research/AutoGaitA/Mouse/Testing/Group 2/",
        # --------------------------
        # RM Dataset (example data in repo)
        # "/Users/mahan/sciebo/PythonCode/gaita_repo/example data/5mm/Results/",
        # "/Users/mahan/sciebo/PythonCode/gaita_repo/example data/12mm/Results/",
        # "/Users/mahan/sciebo/PythonCode/gaita_repo/example data/25mm/Results/",
        # --------------------------
        # Beam x Age for Manuscript
        "/Users/mahan/sciebo/Research/AutoGaitA/Mouse/Full Dataset and Results Nov 2024/5mm/9w",
        "/Users/mahan/sciebo/Research/AutoGaitA/Mouse/Full Dataset and Results Nov 2024/12mm/9w",
        "/Users/mahan/sciebo/Research/AutoGaitA/Mouse/Full Dataset and Results Nov 2024/25mm/9w",
        "/Users/mahan/sciebo/Research/AutoGaitA/Mouse/Full Dataset and Results Nov 2024/5mm/104w",
        "/Users/mahan/sciebo/Research/AutoGaitA/Mouse/Full Dataset and Results Nov 2024/12mm/104w",
        "/Users/mahan/sciebo/Research/AutoGaitA/Mouse/Full Dataset and Results Nov 2024/25mm/104w"
    ]
    folderinfo["results_dir"] = (
        # "/Users/mahan/sciebo/Research/AutoGaitA/Mouse/example_data_results/"
        # "/Users/mahan/sciebo/Research/AutoGaitA/Mouse/Sanity Test Interaction Graziana/Result 10 joints/Mahan Results/"
        # "/Users/mahan/sciebo/Research/AutoGaitA/Mouse/Testing/GroupResults/"
        "/Users/mahan/sciebo/Research/AutoGaitA/Mouse/Full Dataset and Results Nov 2024/YoungOld3BeamsForPaper"
    )
    # cfg
    cfg = {}
    cfg["do_permtest"] = False  # True
    cfg["do_anova"] = True
    cfg["permutation_number"] = 100
    cfg["PCA_n_components"] = 0.9
    cfg["PCA_custom_scatter_PCs"] = "1,3;2,3;2,3,4;;;;"
    cfg["PCA_save_3D_video"] = False
    cfg["PCA_bins"] = ""  # "0-10,24,50-75"
    cfg["stats_threshold"] = 0.05
    cfg["plot_SE"] = True
    cfg["color_palette"] = "inferno"
    cfg["dont_show_plots"] = True
    cfg["legend_outside"] = True
    cfg["which_leg"] = "left"
    cfg["anova_design"] = "RM ANOVA"
    # cfg["anova_design"] = "Mixed ANOVA"
    cfg["PCA_variables"] = [
        # Beam x Age
        "Nose x",
        "Nose y",
        "Ear base x",
        "Ear base y",
        "Front paw tao x",
        "Front paw tao y",
        "Wrist x",
        "Wrist y",
        "Elbow x",
        "Elbow y",
        "Lower Shoulder x",
        "Lower Shoulder y",
        "Upper Shoulder x",
        "Upper Shoulder y",
        "Iliac Crest x",
        "Iliac Crest y",
        "Hip x",
        "Hip y",
        "Knee x",
        "Knee y",
        "Ankle x",
        "Ankle y",
        "Hind paw tao x",
        "Hind paw tao y",
        "Tail base y",
        "Tail center x",
        "Tail center y",
        "Tail tip x",
        "Tail tip y",
        "Hind paw tao Velocity",
        "Hind paw tao Acceleration",
        "Ankle Velocity",
        "Ankle Acceleration",
        "Knee Velocity",
        "Knee Acceleration",
        "Hip Velocity",
        "Hip Acceleration",
        "Iliac Crest Velocity",
        "Iliac Crest Acceleration",
        "Ankle Angle",
        "Knee Angle",
        "Hip Angle",
        "Wrist Angle",
        "Elbow Angle",
        "Lower Shoulder Angle",
        "Iliac Crest Angle",
        "Ankle Angle Velocity",
        "Ankle Angle Acceleration",
        "Knee Angle Acceleration",
        "Hip Angle Velocity",
        "Hip Angle Acceleration",
        "Wrist Angle Velocity",
        "Wrist Angle Acceleration",
        "Elbow Angle Velocity",
        "Elbow Angle Acceleration",
        "Lower Shoulder Angle Velocity",
        "Lower Shoulder Angle Acceleration",
        "Iliac Crest Angle Velocity",
        "Iliac Crest Angle Acceleration",


        # PREVIOUS TESTING FEATURES
        # -----------------
        # "Hind paw tao y",
        # "Ankle y",
        # "Knee y",
        # "Ankle Angle",
        # "Knee Angle",
        # "Nose x",
        # "Knee y",
        # "Knee x",
        # "Knee Velocity",
        # "Knee Acceleration",
        # "Knee Angle",
        # "Knee Angle Velocity",
        # "Knee Angle Acceleration",
        # "Hip Angle",
    ]
    cfg["stats_variables"] = [
        # "Hind paw tao y",
        # "Ankle y",
        # "Knee y",
        # "Ankle Angle",
        # "Knee Angle",
        # "Nose x",
        # "Knee y",
        # "Knee x",
        # "Knee Velocity",
        # "Knee Acceleration",
        # "Knee Angle",
        # "Knee Angle Velocity",
        # "Knee Angle Acceleration",
        # "Hip Angle",
        # "Elbow Angle"


        # Beam x Age
        "Hip x",
        "Hip y",
        "Knee x",
        "Knee y",
        "Ankle x",
        "Ankle y",
        "Hind paw tao x",
        "Hind paw tao y",
        "Hind paw tao Velocity",
        "Ankle Velocity",
        "Knee Velocity",
        "Ankle Angle",
        "Knee Angle",
        "Hip Angle"
    ]
    # run
    autogaita.group(folderinfo, cfg)


# %% what happens if we just hit run
if __name__ == "__main__":
    group_dlcrun()
